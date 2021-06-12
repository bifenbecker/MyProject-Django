from django.urls import path, include
from .views import *


urlpatterns = [
    path('active/', OrderView.as_view(), name='order_view_url'),
    path('history/', HistoryOrderView.as_view(), name='history_order_view_url'),
    path('api/add_to_order', AddToOrderAPI.as_view()),
]