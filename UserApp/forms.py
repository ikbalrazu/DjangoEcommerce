from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, Select, FileInput
from .models import UserProfileModel
from django.contrib.auth.models import User


class user_signup(UserCreationForm):
    username = forms.CharField(max_length=100, label="username", widget=forms.TextInput(attrs={'placeholder':'write your username',}))
    email = forms.EmailField(max_length=200, label="email", widget=forms.EmailInput(attrs={'placeholder':'write your email',}))
    first_name = forms.CharField(max_length=100, label="first_name", widget=forms.TextInput(attrs={'placeholder':'write your first name'}))
    last_name = forms.CharField(max_length=100, label="last_name", widget=forms.TextInput(attrs={'placeholder':'write your last name'}))

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

        widget = {
            'password1':forms.PasswordInput(attrs={'placeholder':'Enter new password','class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'placeholder':'Enter Repeat password','class':'form-control'}),
        }



class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        widgets = {
            'username': TextInput(attrs={'class':'input','placeholder':'Username'}),
            'email': EmailInput(attrs={'class':'input','placeholder':'Email'}),
            'first_name': TextInput(attrs={'class':'input','placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class':'input','placeholder':'Last Name'}),
        }

CITY = [
    ('Dhaka','Dhaka'),
    ('Laxmipur','Laxmipur'),
    ('Dinajpur','Dinajpur'),
]
class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfileModel
        fields = ['phone','address','city','country','image']
        widgets = {

            'phone':TextInput(attrs={'class':'input','placeholder':'Phone Number'}),
            'address':TextInput(attrs={'class':'input','placeholder':'Address'}),
            'city':Select(attrs={'class':'input','placeholder':'City'},choices=CITY),
            'country':TextInput(attrs={'class':'input','placeholder':'Country'}),
            'image':FileInput(attrs={'class':'input','placeholder':'Upload Profile Image'})

        }

