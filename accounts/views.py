from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.models import User

class RegistrationPageView(View):

    def get(self, request):
        model_form = UserForm()
        # model_form.fields['username'].label = 'логин'
        return render(request, 'accounts/registration.html', context={'form': model_form})

    def post(self, request):
        model_form = UserForm(request.POST)
        context = {'form': model_form}
        if model_form.is_valid():
            model_form.save()
            return redirect('login_url')
        else:
            context['error'] = "Неверная форма"
        return render(request, 'accounts/registration.html', context)


class LoginPageView(View):

    def get(self, request):
        model_form = UserForm()
        return render(request, 'accounts/login.html', context={'form':model_form})


    def post(self, request):
        model_form = UserForm(request.POST)

        context = {'form': model_form }
        if model_form.is_valid():
            context['error'] = "Такого пользователя не существует"
        else:
            user = authenticate(request,
                                username=request.POST.get('username'),
                                email=request.POST.get('email'),
                                password=request.POST.get('password'))

            if user is not None:
                login(request, user)
                return redirect('profile_url', user.id)

        return render(request, 'accounts/login.html', context=context)


class ProfilePageView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        if request.user.is_authenticated:
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


