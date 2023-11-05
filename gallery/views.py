from django.shortcuts import get_object_or_404, render, redirect
from .forms import LoginForm
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from .models import Arts
from django.http import HttpResponse
from .models import Video
from .models import Events
from django.contrib.auth.views import PasswordResetView
from .models import TeamMember
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



def home(request):
         return render(request, 'gallery/home.html')


def contact(request):
         return render(request, 'gallery/contact.html')


def about(request):
         return render(request, 'gallery/about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
          #   login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'gallery/signup.html', {'form': form})


def login (request):
     if request.method == 'POST':
          form = LoginForm(request.POST)
          if form.is_valid():
               cd = form.cleaned_data
               user = authenticate(request,
                    username = cd['username'],
                    password = cd['password'])
               if user is not None:
                    if user.is_active:
                         login(request, user)
                         # return redirect('home')
                         return HttpResponse('Autheb=ntucated Successfully')
                    else:
                         return HttpResponse('Disabled user')
               else:
                    return HttpResponse('Invalid login')
     else:
        form = LoginForm()
     return render(request, 'gallery/registration/login.html', {'form':form})


@login_required       
def contact (request):
     return render(request, 'gallery/contact.html')


@login_required
def about(request):
    return render(request, 'gallery/about.html')


@login_required
def artwork(request):
      art= Arts.objects.all()
      context= {"art": art}
      return render(request, 'gallery/gallery.html', context)


@login_required
def elearning(request):
    videos = Video.objects.all()
    context = {"videos":videos}
    return render( request, 'gallery/elearning.html', context)


@login_required
def team(request):
    team_members = TeamMember.objects.all()
    return render(request, 'gallery/team.html', {'team': team_members})


@login_required
def blog(request):
     events = Events.objects.all()
     return render(request, 'gallery/blog.html', {'events': events})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'gallery/password_reset.html'
    email_template_name = 'gallery/password_reset_email.html'
    success_url = '/password_reset/done/'
    

@csrf_exempt
@login_required
def index(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        quantity = int(request.POST.get("quantity"))
        total_amount = round(amount * quantity)

        phone_number = request.POST.get("phone")
        art_name = request.POST.get("artwork")
        print(art_name)

        # user = request.user
        # print(user)

        # cache.set("user", user)
        # cache.set("art_name", art_name )
        # print(art_name, user)
        
        cl = MpesaClient()
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = "https://9922-105-161-150-135.ngrok-free.app/payment_result/"
        response = cl.stk_push(
            phone_number, total_amount, account_reference, transaction_desc, callback_url
        )
        return HttpResponse(response)

    return HttpResponse("Invalid request")


@csrf_exempt
def payment_result(request):
    cl = MpesaClient()
    if request.method == "POST":
        result = cl.parse_stk_result(request.body)
        if result["ResultCode"] == 0:
            amount = result.get("Amount")
            receipt_no = result.get("MpesaReceiptNumber")
            transaction_date = result.get("TransactionDate")
            phone_number = result.get("PhoneNumber")
            print(amount)

            number = str(phone_number)
            transaction_date_str = str(transaction_date)
            transaction_date = datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")

            print(receipt_no,number,amount,transaction_date)
            transaction = Transaction.objects.create(
                receipt_no=receipt_no,
                sender_no=number,
                amount=amount,
                transaction_date=transaction_date,
                status="Complete"
            )


            # Render the HTML template with the payment details
            return render(request, 'gallery/payment_result.html', {
                'amount': amount,
                'receipt_number': receipt_no,
                'transaction_date': transaction_date,
                'phone_number': phone_number
            })

    return HttpResponse("okay")

def payment_process(request):
    phone_number = request.GET.get('phone_number')
    price = request.GET.get('price')

    context = {
        'phone_number': phone_number,
        'price': price,
    }
    return render(request, 'gallery/payment.html', context)


def payment_form(request):
    art_id = request.GET.get("art_id")
    art = get_object_or_404(Arts, pk=art_id)
    context = {"art": art}
    return render(request, 'gallery/payment_form.html', context)
    
    
def payment_success(request):
    return render(request, 'gallery/payment_success.html')



from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from .models import User, Events, Arts, Transaction,TeamMember
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from .models import Events, Arts, Transaction,TeamMember
from django.contrib.auth.models import User


def generate_report(request):
    # Checks if the form is submitted
    if request.method == 'POST':
        report_type = request.POST.get('report_type')

        if report_type == 'users':
            return generate_users_report()
        elif report_type == 'events':
            return generate_events_report()
        elif report_type == 'arts':
            return generate_arts_report()
        elif report_type == 'transactions':
            return generate_transactions_report()

    return render(request, 'gallery/generate_report.html')


def generate_users_report():
    # Get the data for the report (e.g., users)
    users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')

    # Create a response object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users_report.pdf"'

    # Create the PDF document using ReportLab
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add the report title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph('ARTHUB', title_style))
    elements.append(Paragraph('Users Report', title_style))

    # Add the logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'gallery', 'img', 'favicon.png')
    logo = Image(logo_path, width=100, height=100)
    elements.append(logo)

    # Create the table data
    table_data = [('Username', 'First Name', 'Last Name', 'Email')]
    table_data.extend(users)

    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid color
    ])

    # Create the table
    table = Table(table_data)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response


# Update the other report generation functions (generate_events_report, generate_arts_report, generate_transactions_report)
# in a similar manner to include the logo.


def generate_events_report():
    # Get the data for the report (e.g., events)
    events = Events.objects.all().values_list('title', 'date', 'time', 'location', 'description')

    # Create a response object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="events_report.pdf"'

    # Create the PDF document using ReportLab
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add the report title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph('ARTHUB', title_style))
    elements.append(Paragraph('Events Report', title_style))

    # Add the logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'gallery', 'img', 'favicon.png')
    logo = Image(logo_path, width=100, height=100)
    elements.append(logo)

    # Create the table data
    table_data = [('Title', 'Date', 'Time', 'Location', 'Description')]
    table_data.extend(events)

    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid color
    ])

    # Create the table
    table = Table(table_data)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response


def generate_arts_report():
    # Get the data for the report (e.g., arts)
    arts = Arts.objects.all().values_list('title', 'art_id', 'cost', 'description')

    # Create a response object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="arts_report.pdf"'

    # Create the PDF document using ReportLab
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add the report title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph('ARTHUB', title_style))
    elements.append(Paragraph('Arts Report', title_style))

    # Add the logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'gallery', 'img', 'favicon.png')
    logo = Image(logo_path, width=100, height=100)
    elements.append(logo)

    # Create the table data
    table_data = [('Title', 'Art ID', 'Cost', 'Description')]
    table_data.extend(arts)

    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid color
    ])

    # Create the table
    table = Table(table_data)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response


def generate_transactions_report():
    # Get the data for the report (e.g., transactions)
    transactions = Transaction.objects.all().values_list('id', 'receipt_no', 'sender_no', 'amount', 'transaction_date', 'status')

    # Create a response object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions_report.pdf"'

    # Create the PDF document using ReportLab
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add the report title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph('ARTHUB', title_style))
    elements.append(Paragraph('Transactions Report', title_style))

    # Add the logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'gallery', 'img', 'favicon.png')
    logo = Image(logo_path, width=100, height=100)
    elements.append(logo)

    # Create the table data
    table_data = [('No', 'Transaction code', 'Sender Number', 'Total Price', 'Date and Time','Status')]
    table_data.extend(transactions)

    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid color
    ])

    # Create the table
    table = Table(table_data)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response

