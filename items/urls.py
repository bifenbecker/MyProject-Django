from django.urls import path, include
from .views import *


urlpatterns = [
    path('search/', search_view, name='search_url'),
    path('categories/', CategoriesView.as_view(), name='categories_url'),
    path('categories/<slug>', CategoriesDetailView.as_view(), name='category_url'),
    path('api/get_items', GetItemAPI.as_view()),
]
