from django.urls import path, include
from .views import *


urlpatterns = [
    path('active/', OrderView.as_view(), name='order_view_url'),
    path('history/', HistoryOrderView.as_view(), name='history_order_view_url'),
    path('api/add_item_to_order', AddToOrderAPIView.as_view()),
    path('api/remove_item_from_order', RemoveFromOrderAPIView.as_view()),
    path('api/change_item_qty_in_order', ChangeItemQuantityInOrderAPIView.as_view()),
    path('api/close_order', CloseOrderAPIView.as_view()),
]