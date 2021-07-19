from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class LoginForm(AuthenticationForm):
    username = None
    email = forms.EmailField(max_length=75, required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Введите E-Mail адрес...'}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Пароль', 'autocomplete': 'current-password'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, email=email, password=password)
            if self.user_cache is None:
                raise ValidationError('Неверная почта и пароль', code='invalid_login')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError('Аккаунт заблокирован', code='inactive')

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=75, required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'E-Mail адрес'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Пароль'}))
    confirm_password = forms.CharField(max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Пароль (ещё раз)'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f"Аккаунт с таким адресом уже существует")

        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        return self.cleaned_data


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(max_length=128, required=True,
                             widget=forms.PasswordInput(
                                 attrs={'class': 'form-control form-control-user', 'placeholder': 'Старый пароль'}))
    new_password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control form-control-user', 'placeholder': 'Новый пароль'}))
    confirm_new_password = forms.CharField(max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                         'placeholder': 'Новый пароль (ещё раз)'}))

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password'].label = "Новый пароль"
        self.fields['confirm_new_password'].label = "Новый пароль (еще раз)"
        self.user = user

    def clean(self):
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password != confirm_new_password:
            raise forms.ValidationError("Пароли не совпадают")

        if confirm_new_password == old_password or new_password == old_password:
            raise forms.ValidationError("Придуймайте новый пароль. Новый пароль совпадает со старым")

        if self.user.check_password(old_password) == False:
            raise forms.ValidationError("Старый пароль веден неверно")

        return self.cleaned_data


class UsernameChangeForm(forms.ModelForm):
    new_username = forms.CharField(max_length=128, required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control form-control-user', 'placeholder': 'Новое имя пользователя'}))


    class Meta:
        model = get_user_model()
        fields = ['new_username']

    def __init__(self, user, *args, **kwargs):
        super(UsernameChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_username'].label = "Новое имя пользователя"
        self.user = user

    def clean(self):
        username = self.user.username
        if self.cleaned_data['new_username'] == username:
            raise forms.ValidationError("У Вас такое имя сейчас")

        return self.cleaned_data

