from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.contrib.auth.models import User

class RegistrationPageView(View):
    template_name = 'accounts/registration.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self,request):
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.username = form.cleaned_data['email'].split("@")[0]
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('profile_url', new_user.id)
        return render(request, self.template_name, context={'form': form})


class LoginPageView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = authenticate(username=username, email=email, password=password)
            if user:
                login(request, user)
                return redirect('profile_url', user.id)
        return render(request, self.template_name, context={'form': form})


class ProfilePageView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        if user.is_authenticated:
            return render(request, 'accounts/profile.html', context={'user':user})
        else:
            return redirect('login_url')


class LogoutPageView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('index')
        else:
            return redirect('login_url')


