from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include
import accounts.views as views

urlpatterns = [
    path('registration/', views.RegistrationPageView.as_view(), name='registration_url'),
    path('login/', views.LoginPageView.as_view(), name='login_url'),
    path('logout/', views.LogoutPageView.as_view(), name='logout_url'),
    path('profile/', views.ProfileView.as_view(), name='profile_url'),
    path('password-change/', views.ProfilePasswordChangeView.as_view(), name='password_change_url'),
    path('username_change/', views.ProfileUsernameChangeView.as_view(), name='username_change_url'),
]