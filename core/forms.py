from django import forms
from core.models import User


class RegisterUser(forms.form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    
