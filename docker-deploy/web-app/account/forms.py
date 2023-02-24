from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import MyUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')

class BasicUserChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')

class NonDriverForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone_number', )

class DriverProfForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone_number', )
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'phone_number': forms.TextInput(attrs={'required': True}),
        }