from django.urls import path, include
from .views import search_view


urlpatterns = [
    path('search/', search_view, name='search_url'),
]
