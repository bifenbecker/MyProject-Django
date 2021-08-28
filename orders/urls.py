from django.urls import path, include
from .views import *


urlpatterns = [
    path('active/', OrderView.as_view(), name='order_view_url'),
    path('active-forming/', FormingOrderView.as_view(), name='forming-order_view_url'),
    path('history/', HistoryOrderView.as_view(), name='history_order_view_url'),
    path('history/<int:order_id>', HistoryOrderDetailView.as_view(), name='history_order_detail_view_url'),
    path('api/add_product_to_order', AddToOrderAPIView.as_view()),
    path('api/remove_item_from_order', RemoveItemFromOrderAPIView.as_view()),
    path('api/remove_product_from_order', RemoveProductFromOrderAPIView.as_view()),
    path('api/change_item_qty_in_order', ChangeItemQuantityInOrderAPIView.as_view()),
    path('api/change_product_qty_in_order', ChangeProductQuantityInOrderAPIView.as_view()),
    path('api/close_order', CloseOrderAPIView.as_view()),
    path('api/price_history', PriceHistoryOrderAPI.as_view()),
    path('api/set_active_order', SetActiveOrderAPI.as_view()),
    path('api/send_message_to_suppliers', SendMessageToSuppliers.as_view()),
    path('api/make-order', MakeOrderAPI.as_view()),
]