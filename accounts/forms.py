from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'style':'width:25%'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'style':'width:25%'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'style':'width:25%'},)
        }