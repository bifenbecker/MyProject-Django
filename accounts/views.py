from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout


from Pilaru import settings
from .forms import LoginForm, RegistrationForm, PasswordChangeForm, UsernameChangeForm
from .models import User


class RegistrationPageView(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.username = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('search_url')
        return render(request, self.template_name, context={'form': form})


class LoginPageView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class LogoutPageView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('index_url')
        else:
            return redirect('login_url')


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Профиль',
            'toolbar_title': 'Профиль - ' + user.username,
            'user': user
        }
        return render(request, self.template_name, context=context)


class ProfilePasswordChangeView(View):
    template_name = 'password_change_form.html'

    context = {
        'page_title': settings.PAGE_TITLE_PREFIX + 'Изменить пароль',
        'toolbar_title': 'Изменить пароль',
    }

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST or None)
        self.context.update({'form': form})
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST or None)
        self.context.update({'form': form})
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            return redirect('login_url')
        return render(request, self.template_name, context=self.context)


class ProfileUsernameChangeView(View):
    template_name = 'username_change_form.html'

    context = {
        'page_title': settings.PAGE_TITLE_PREFIX + 'Изменить имя пользователя',
        'toolbar_title': 'Изменить имя пользователя',
    }

    def get(self, request, *args, **kwargs):
        form = UsernameChangeForm(request.user, request.POST or None)
        self.context.update({'form': form})
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = UsernameChangeForm(request.user, request.POST or None)
        self.context.update({'form': form})
        if form.is_valid():
            request.user.username = form.cleaned_data['new_username']
            request.user.save()
            return redirect('profile_url')
        return render(request, self.template_name, context=self.context)




