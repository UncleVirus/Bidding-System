from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password =models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']



class Arts(models.Model):
      art_id = models.AutoField(primary_key=True)
      picture = models.ImageField(upload_to='artwork_images/')
      title = models.CharField(max_length=100)
      description = models.TextField()
      cost = models.DecimalField(max_digits=10, decimal_places=2)
      is_available = models.BooleanField(default=True)

      def __str__(self):
         return self.title
      

class Video(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    video_file = models.FileField(upload_to ='videos/')

    def __str__(self):
        return self.title
    

class Events(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to= 'events/images/')
    video = models.FileField(upload_to= 'events/video/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    

class TeamMember(models.Model) :
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'team_images')
    member_Id = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name

    
class Transaction(models.Model):
    receipt_no = models.CharField(max_length=255)
    sender_no = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Complete")
