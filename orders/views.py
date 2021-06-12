from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView

from items.models import Item
from .models import Order, ItemToOrder


# region Views
from .serializer import ItemToOrderSerializer


# TODO View only active order
class OrderView(View):
    template_name = 'order_view.html'

    def get(self, request, *args, **kwargs):
        order_list = request.user.orders.all()

        return render(request, self.template_name, context={'order_list': order_list})


# TODO Create order history
class HistoryOrderView(View):
    template_name = 'history_order_view.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)
# endregion


# region API
class AddToOrderAPI(APIView):
    """
    Добавление товара в заказ
    """
    def post(self, request):
        """
        POST запрос 'domain/orders/api/add_to_order'
        Ключи словаря
        item_id = ID товара
        quantity = Количество товара
        """

        try:
            data = request.data
            quantity = data['quantity']
            user = request.user
            # Item
            item_id = data['item_id']

            try:
                additional_item = Item.objects.get(id=item_id)
            except ObjectDoesNotExist:
                raise Exception("Товар не найден")

            # Order
            order = user.active_order

            # Create order if does not exists
            if not order:
                order = Order.objects.create(created_by=request.user)

            new_item = ItemToOrder.objects.create(
                item=additional_item,
                order=order,
                quantity=quantity
            )

            serializerItemToOrder = ItemToOrderSerializer(new_item)

            return Response({'Result': serializerItemToOrder.data})
        except Exception as e:
            return Response({'Result': str(e)})
# endregion