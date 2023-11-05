from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from flask import Flask, render_template, request

class LoginForm(forms.Form):
    username = forms.CharField(max_length=8)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', 'first_name', 'last_name')  


# class paymentform(forms.Forms):
#     artwork_id = forms.CharField()
#     name = forms.CharField(max_length=100)
#     phone_no = forms.


    