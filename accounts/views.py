from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegistrationForm
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


# TODO: Need test with few profiles
class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, context={"user": user})



