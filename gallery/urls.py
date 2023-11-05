
from django.urls import path, include
from . import views
from .views import signup
from django.conf import settings
from django.conf.urls.static import static
from .views import elearning
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views
from .views import team
from .views import generate_users_report
# from .views import payment

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('signup/',signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('artwork/', views.artwork, name='artwork'),
    path('about/', views.about, name='about'),
    path('elearning/', elearning, name='elearning'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='gallery/password_reset.html'), name='password_reset'),
    path('blog/', views.blog, name='blog'),
    path('team/', team, name= 'team'),
    path('index/', views.index, name= 'index'),
    path('payment_process/', views.payment_process, name='payment_process'),
    path('payment_result/', views.payment_result, name='payment_result'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_form/', views.payment_form, name= 'payment_form'),
    path('generate-report/', views.generate_report, name='generate_report'),


   ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
    
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # Other URL patterns

