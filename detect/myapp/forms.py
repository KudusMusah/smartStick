from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import StickInfo


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        


class StickInfoForm(forms.ModelForm):
    class Meta:
        model = StickInfo
        fields = '__all__'
        exclude = ["stick",]