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



def get_history_order(orders):
    try:
        history_order_by_user = []
        _state = OrderState.objects.filter(name='Активный').first()
        for _order in orders:
            _orders = OrderStateToOrder.objects.filter(state=_state, order=_order, finished_date__isnull=False)
            if len(_orders) > 0:
                for o in _orders:
                    history_order_by_user.append(o)

        if len(history_order_by_user) != 0:
            return history_order_by_user
        else:
            raise ObjectDoesNotExist("У Вас пока нет истории заказов :(")
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("У Вас пока нет истории заказов :(")


def find_last_item_price_and_supplier_in_orders(item: ItemToOrder, orders: list):
    orders = orders[::-1]
    for order in orders:
        for item_in_order in order.order.items_in_order.all():
            if item_in_order.item.supplier.name == item.item.supplier.name and item_in_order.item.name == item.item.name:
                return (float(item_in_order.price_offer.price_per_unit), item_in_order.item.supplier.name)

    return 0.0


def get_last_price_by_order(user, order):
    last_price = {}
    orders = user.orders.all()
    try:
        history_order_by_user = get_history_order(orders)
        for item_in_active_order in order.items_in_order.all():
            last_price[item_in_active_order.id] = find_last_item_price_and_supplier_in_orders(
                item_in_active_order,
                history_order_by_user)
    except ObjectDoesNotExist as e:
        for item_in_active_order in order.items_in_order.all():
            last_price[item_in_active_order.id] = (str(e), '')

    return last_price


def is_auth(func):
    """Check is authenticated user"""

    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(self, request, *args, **kwargs)
        else:
            return redirect('login_url')
    return wrapper


# region Views
class OrderView(View):

    @is_auth
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Текущие заказы',
            'toolbar_title': 'Текущие заказы с проектов'
        }

        active_orders_by_projects = []
        for member in request.user.member_in_projects.all():
            if member.project.get_active_order():
                active_orders_by_projects.append(member.project.get_active_order())

        last_price_orders = {}
        if len(active_orders_by_projects) != 0:
            for order in active_orders_by_projects:
                last_price_orders.update({order.id: get_last_price_by_order(request.user, order)})

        if len(active_orders_by_projects) != 0:
            context['active_orders'] = active_orders_by_projects
            context['last_price'] = last_price_orders
            stages = Stage.objects.all()
            context['stages'] = stages
            return render(request, 'order_view.html', context=context)
        else:
            return render(request, 'order_view__no_active.html', context=context)


class HistoryOrderView(View):
    template_name = 'history_order_view.html'

    @is_auth
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Заказы',
            'toolbar_title': 'История заказов',
        }
        try:
            orders = request.user.orders.all()
            history_order_by_user = get_history_order(orders)
            context.update({'order_list': history_order_by_user})
            return render(request, self.template_name, context=context)
        except ObjectDoesNotExist as e:
            context.update({'error': str(e)})
            return render(request, self.template_name, context=context)


class HistoryOrderDetailView(View):
    template_name = "history_order_detail_view.html"

    @is_auth
    def get(self, request, *args, **kwargs):
        order_id = kwargs['order_id']

        order_state_to_order = OrderStateToOrder.objects.get(id=order_id)
        order = Order.objects.get(id=order_state_to_order.order_id)

        if order.created_by == request.user:
            context = {
                'page_title': settings.PAGE_TITLE_PREFIX + 'Заказ: ' + str(order.id),
                'toolbar_title': 'Заказ: ' + str(order.id) + ' От ' + str(order.created_date).split(".")[0]
            }
            context['active_order'] = order
            return render(request, self.template_name, context=context)

        # Protect order
        # TODO: make error
        # else:


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
            order = user.active_order
            # Create order if does not exists
            # TODO: Need to check on bugs
            if order is None:
                # if len(user.member_in_projects.all()) == 0:
                #     redirect('create_project_url')
                #     return Response({'error': 'Create'})

                active_project = user.get_active_project()
                if active_project is None:
                    return Response({'result': 'Создайте или вступите в проект'})

                order = Order.objects.create(created_by=request.user, project=active_project) # Автоматически добавлять товар в новый заказ в активном(последнем) проекте (Без выбора)
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
                item_to_order.price_offer = PriceOffer.objects.get_or_create(
                    item=item,
                    for_quantity=random.randint(10, 50),
                    price_per_unit=Decimal(random.randrange(1, 200, 1)),
                )[0]
                item_to_order.save()


            return Response({'result': 'ok'})
        except Exception as e:
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

            order.set_order_state(OrderState.objects.get(name='Отменен'))

            return Response({'result': 'ok'})
        except Exception as e:
            print(e)
            return Response('error', status=500)


class PriceHistoryOrderAPI(APIView):

    def post(self, request):
        data = request.data
        item_name = data['name']
        item_supplier = data['supplier']
        orders = request.user.orders.all()

        data_of_item = {}
        for order in orders:
            for item_in_order in order.items_in_order.all():
                if item_in_order.item.supplier.name == item_supplier and item_in_order.item.name == item_name:
                    date = str(item_in_order.created_date).split(".")[0]
                    try:
                        data_of_item[date] = float(item_in_order.price_offer.price_per_unit)
                    except:
                        data_of_item[date] = 0

        return Response({'Result': 'ok', 'Data': data_of_item})


class SetActiveOrderAPI(APIView):

    def post(self, request):
        data = request.data
        order = Order.objects.get(id=data['order_id'])
        if order.project.name != data['project_name']:
            return Response({'error': 'Неизвестная ошибка'})
        request.user.set_active_order(order)
        return Response({'Result': 'ok'})
# endregion
