from django.urls import path, include
from .views import index_view, handle_404_view


urlpatterns = [
    path('', index_view, name='index_url'),
    path('404/', handle_404_view, name='404_url'),
]
