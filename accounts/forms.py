from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=75, required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'style':'width:25%'}))

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control', 'style':'width:25%'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Почта'
        self.fields['password'].label = 'Пароль'


    def clean_email(self):
        email = self.cleaned_data['email']

        if "@" not in email:
            raise forms.ValidationError("Неверный формат почты")
        return email

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с почтой {email} не найден')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(max_length=75, required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:25%'}))
    confirm_password = forms.CharField(max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={'class':'form-control', 'style':'width:25%'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'style':'width:25%'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']


    def clean_email(self):
        email = self.cleaned_data['email']
        if "@" not in email:
            raise forms.ValidationError("Неверный формат почты")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Аккаунт почтой - {email} уже существует")

        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        return self.cleaned_data



