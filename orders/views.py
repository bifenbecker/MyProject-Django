from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from items.models import Item
from .models import Order, Stage, ItemToOrder, OrderState, OrderStateToOrder, PriceOffer

import random
from decimal import Decimal


# region Views
class OrderView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Текущий заказ',
            'toolbar_title': 'Текущий заказ'
        }

        active_order = request.user.get_active_order()
        if active_order:
            context['active_order'] = active_order
            return render(request, 'order_view.html', context=context)
        else:
            return render(request, 'order_view__no_active.html', context=context)


class HistoryOrderView(View):
    template_name = 'history_order_view.html'

    def get(self, request, *args, **kwargs):
        try:
            history_order_by_user = []
            orders = Order.objects.filter(created_by=request.user)
            _state = OrderState.objects.filter(name='Активный').first()

            for _order in orders:
                _orders = OrderStateToOrder.objects.filter(state=_state, order=_order, finished_date__isnull=False)
                if len(_orders) > 0:
                    for o in _orders:
                        history_order_by_user.append(o)

            return render(request, self.template_name, context={'order_list': history_order_by_user})
        except ObjectDoesNotExist:
            return render(request, self.template_name, context={'error': "У Вас пока нет истории заказов :("})


class HistoryOrderDetailView(View):
    template_name = "order_view.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Текущий заказ',
            'toolbar_title': 'Текущий заказ'
        }
        order = OrderStateToOrder.objects.get(id=order_id)
        context['active_order'] = Order.objects.get(id=order.order_id)
        return render(request, self.template_name, context=context)
# endregion


# region API
class AddToOrderAPIView(APIView):
    """
    Добавление товара в заказ
    """
    def post(self, request):
        """
        POST запрос 'domain/orders/api/add_item_to_order'
        Ключи словаря
        item_id = ID товара
        quantity = Количество товара
        """

        try:
            data = request.data
            quantity = int(data['quantity'])
            user = request.user
            item_id = int(data['item_id'])

            try:
                item = Item.objects.get(id=item_id)
            except ObjectDoesNotExist:
                raise Exception("Товар не найден")

            # Order
            order = user.get_active_order()
            # Create order if does not exists
            if order is None:
                order = Order.objects.create(created_by=request.user)
                order_state = OrderState.objects.get(name='Активный')
                OrderStateToOrder.objects.create(order=order, state=order_state)

            item_to_order = ItemToOrder.objects.filter(item=item, order=order).first()

            if item_to_order:
                item_to_order.quantity += quantity
                item_to_order.save()
            else:
                item_to_order = ItemToOrder.objects.create(
                    item=item,
                    order=order,
                    quantity=quantity,
                    stage=Stage.objects.all()[0]
                )
                if random.random() > 0.6:
                    item_to_order.price_offer = PriceOffer.objects.get_or_create(
                        item=item,
                        for_quantity=random.randint(10, 50),
                        price_per_unit=Decimal(random.randrange(1, 200, 1)),
                    )[0]
                    item_to_order.save()

            return Response({'result': 'ok'})
        except Exception as e:
            print(e)
            return Response('error', status=500)


class RemoveFromOrderAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            item_to_order_id = data['item_to_order_id']

            try:
                item_to_order = ItemToOrder.objects.get(id=item_to_order_id)
            except ObjectDoesNotExist:
                raise Exception("Товар не найден")
            item_to_order.delete()

            return Response({'result': 'ok'})
        except Exception as e:
            print(e)
            return Response('error', status=500)


class ChangeItemQuantityInOrderAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            item_to_order_id = data['item_to_order_id']
            new_quantity = int(data['quantity'])

            try:
                item_to_order = ItemToOrder.objects.get(id=item_to_order_id)
            except ObjectDoesNotExist:
                raise Exception("Товар не найден")
            item_to_order.quantity = new_quantity
            item_to_order.save()

            return Response({'result': 'ok'})
        except Exception as e:
            print(e)
            return Response('error', status=500)


class CloseOrderAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            order_id = data['order_id']

            try:
                order = Order.objects.get(id=order_id)
            except ObjectDoesNotExist:
                raise Exception("Заказ не найден")

            order.set_order_state(OrderState.objects.get(name='Закрыт'))

            return Response({'result': 'ok'})
        except Exception as e:
            print(e)
            return Response('error', status=500)

# endregion
