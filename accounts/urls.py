from django.urls import path, include
from .views import *

urlpatterns = [
    path('registration/', RegistrationPageView.as_view(), name='registration_url'),
    path('login/', LoginPageView.as_view(), name='login_url'),
    path('profile/<id>/', ProfilePageView.as_view(), name='profile_url'),
    path('logout/', LogoutPageView.as_view(), name='logout_url')
]