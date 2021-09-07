from time import sleep

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import imaplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from rest_framework.response import Response
from rest_framework.views import APIView


from items.models import Item, Product, Supplier, SupplierContact
from .models import Order, Stage, ItemToOrder, OrderState, OrderStateToOrder, PriceOffer, ProductToOrder

import random
from decimal import Decimal



def get_history_order(user):
    try:
        history_order = []
        for order in user.orders.all():
            if not order.is_active():
                history_order.append(order)

        if len(history_order) == 0:
            raise ObjectDoesNotExist("У Вас пока нет истории заказов :(")
        else:
            return history_order
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("У Вас пока нет истории заказов :(")


def find_last_item_price_from_supplier_in_orders(item: Item, orders: list):
    for order in orders:
        for item_in_order in order.items_in_order.all():
            if item_in_order.item.supplier.name == item.supplier.name and item_in_order.item.name == item.name:
                return float(item_in_order.price_offer.price_per_unit)

    return "Такого товара не было ранее"


def get_last_price_by_order(user, order):
    last_price = {}

    try:
        history_order_by_user = get_history_order(user)
        if len(order.items_in_order.all()) != 0:
            for item_in_active_order in order.items_in_order.all():
                last_price[item_in_active_order.id] = find_last_item_price_from_supplier_in_orders(
                    item_in_active_order.item,
                    history_order_by_user)
        else:
            for product in order.products_in_order.all():
                for item_in_product in product.product.items.all():
                    last_price[item_in_product.id] = find_last_item_price_from_supplier_in_orders(
                        item_in_product,
                        history_order_by_user)

    except Exception as e:
        # TODO: Need to check
        # for item_in_active_order in order.items_in_order.all():
        #     last_price[item_in_active_order.id] = (str(e), '')
        # for product_in_order in order.products_in_order.all():
        #     for item in product_in_order.product.items.all():
        #         last_price[item.id] = (str(e), '')
        for product_in_order in order.products_in_order.all():
            for item in product_in_order.product.items.all():
                last_price[item.id] = str(e)

    return last_price if last_price else None


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


class FormingOrderView(View):
    template_name = "order_view.html"

    @is_auth
    def get(self, request):
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
                for item_in_order in order.items_in_order.all():
                    # if order.order_stage != 1:
                    #     print(item_in_order.get_last_price(request.user))
                    last_price_orders.update({order.id: get_last_price_by_order(request.user, order)})

        if len(active_orders_by_projects) != 0:
            context['orders'] = active_orders_by_projects
            context['last_price'] = last_price_orders
            context['stages'] = Stage.objects.all()
            return render(request, self.template_name, context=context)
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
            context.update({'order_list': orders})
            return render(request, self.template_name, context=context)
        except ObjectDoesNotExist as e:
            context.update({'error': str(e)})
            return render(request, self.template_name, context=context)


class HistoryOrderDetailView(View):
    template_name = "history_order_detail_view.html"

    @is_auth
    def get(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        state_order = "Закрыт" if order.is_closed() else "Завершён"

        if order.created_by == request.user:
            context = {
                'page_title': settings.PAGE_TITLE_PREFIX + 'Заказ: ' + str(order.id),
                'toolbar_title': 'Заказ: ' + str(order.id) + ' От ' + str(order.created_date).split(".")[0] + " (" + state_order + ")"
            }
            context['order'] = order
            return render(request, self.template_name, context=context)

# endregion


# region API
class AddToOrderAPIView(APIView):
    """
    Добавление продукта в заказ
    """
    def post(self, request):
        """
        POST запрос 'domain/orders/api/add_product_to_order'
        Ключи словаря
        product_id = ID продукта
        """

        try:
            data = request.data
            user = request.user
            product_id = int(data['product_id'])

            try:
                product = Product.objects.get(id=product_id)
            except ObjectDoesNotExist:
                raise Exception("Товар не найден")

            # Order
            order = user.active_order

            # Create order if does not exists
            # TODO: Need to check on bugs
            if order is None:
                if user.get_active_orders_from_projects() > 0:
                    return Response({'result': 'Выберите заказ с проекта'})
                active_project = user.get_active_project()
                if active_project is None:
                    return Response({'result': 'Создайте или вступите в проект'})

                order = Order.objects.create(created_by=request.user, project=active_project) # Автоматически добавлять товар в новый заказ в активном(последнем) проекте (Без выбора)
                order_state = OrderState.objects.get(name='Активный')
                OrderStateToOrder.objects.create(order=order, state=order_state)

            product_to_order = ProductToOrder.objects.filter(product=product, order=order).first()

            if product_to_order:
                product_to_order.save()
            else:
                product_to_order = ProductToOrder.objects.create(
                    product=product,
                    order=order,
                )
                product_to_order.save()


            return Response({'result': 'ok'})
        except Exception as e:
            return Response('error', status=500)


class RemoveItemFromOrderAPIView(APIView):

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


class RemoveProductFromOrderAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            product_to_order_id = data['product_to_order_id']
            try:
                product_to_order = ProductToOrder.objects.get(id=product_to_order_id)
            except ObjectDoesNotExist:
                raise Exception("Продукт не найден")
            product_to_order.delete()

            return Response({'result': 'ok'})
        except Exception as e:
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


class ChangeProductQuantityInOrderAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            product_to_order_id = data['product_to_order_id']
            new_quantity = int(data['quantity'])

            try:
                product_to_order = ProductToOrder.objects.get(id=product_to_order_id)
            except ObjectDoesNotExist:
                raise Response({'error': "Продукт не найден"})
            product_to_order.quantity = new_quantity
            product_to_order.save()

            return Response({'result': 'ok'})
        except Exception as e:
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

            if order == request.user.active_order:
                request.user.active_order = None
                request.user.save()

            return Response({'result': 'ok'})
        except Exception as e:
            return Response('error', status=500)


class PriceHistoryOrderAPI(APIView):

    def post(self, request):
        data = request.data
        item_id = int(data['item_id'])
        orders = request.user.orders.all()

        data_of_item = {}
        for order in orders:
            for item_in_order in order.items_in_order.all():
                if item_in_order.item.id == item_id:
                    date = str(item_in_order.created_date).split(".")[0]
                    try:
                        data_of_item[date] = float(item_in_order.price_offer.price_per_unit)
                    except:
                        data_of_item[date] = 0

        return Response({'Result': 'ok', 'Data': data_of_item})


class SetActiveOrderAPI(APIView):

    def post(self, request):
        data = request.data
        to_set_active_order = Order.objects.get(id=data['set_active_order_id'])
        request.user.set_active_order(to_set_active_order)
        orders = {
            'active': to_set_active_order.id,
            'non-active': [],
        }
        for member_in_project in request.user.member_in_projects.all():
            active_order_in_project = member_in_project.project.get_active_order()
            if active_order_in_project and active_order_in_project.id != to_set_active_order.id:
                orders['non-active'].append(active_order_in_project.id)

        return Response(orders)


TEST_SUPPLIER_MAIL = 'supplier_test_1@mail.ru'
TEST_SUPPLIER_PASSWORD = 'test_supplier'
TEST_SUPPLIER_NAME = 'Очаг'

TEST_USER_MAIL = 'user_test_4@mail.ru'
TEST_USER_PASSWORD = 'test_user'


class SendMessageToSuppliers(APIView):
    """
    API запроса цены у поставщиков
    """
    def post(self, request):
        """
        /orders/api/send_message_to_suppliers
        :param request:
        order_id: ID Заказа
        qtn_data: Количество
        :return:
        """
        import json

        # TODO: Need to change random price to send request to suppliers
        data = request.data
        order_id = data['order_id']
        qtn_data = json.loads(data['qtn_data'])

        order = Order.objects.get(id=order_id)

        text = """
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
            </head>
            <body>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
            <div class="row justify-content-center">
                <div class="col-10">
                    <h5>Заказ с проекта - {0}</h5>
                    <div class="card shadow mb-4">
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-bordered w-100" cellspacing="0">
                                            <thead>
                                            <tr>
                                                <th>Номер</th>
                                                <th>Название</th>
                                                <th>Этап</th>
                                                <th>Единица измерения</th>
                                                <th>Колчисетво</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {1}
                                            </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </body>
        </html>
        """
        row_table = """
            <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>  
                <td>{4}</td>                       
            </tr>                       
        """

        data_suppliers = {}
        if order.order_stage == 1:
            try:
                for product_in_order in order.products_in_order.all():
                    for item_in_order in product_in_order.product.items.all():
                        try:
                            item_to_order = ItemToOrder.objects.get(
                                item=item_in_order,
                                order=order,
                                quantity=qtn_data[str(item_in_order.id)]
                            )
                        except:
                            item_to_order = None

                        if not item_to_order:
                            item_to_order = ItemToOrder.objects.create(
                                item=item_in_order,
                                order=order,
                                quantity=qtn_data[str(item_in_order.id)],
                            )

                        try:
                            if item_in_order.supplier in data_suppliers.keys():
                                data_suppliers[item_in_order.supplier][0].append(item_to_order)
                            else:
                                data_suppliers.update(
                                    {item_in_order.supplier: ([item_to_order], product_in_order.stage)})

                        except Exception as e:
                            print(str(e))

                for supplier in data_suppliers:
                    # TODO: Какой контакт использовать
                    supplier_contact = supplier.contacts.all().first()
                    try:
                        html_message = render_to_string('message_to_suppliers.html', context={'rows' : data_suppliers[supplier][0], 'stage': data_suppliers[supplier][1], 'project_name': order.project.name})
                    except Exception as e:
                        print(str(e))
                    # msg = MIMEMultipart('alternative')
                    # msg['Subject'] = "Запрос цены"
                    # msg['From'] = settings.EMAIL_HOST_USER
                    # msg['To'] = (supplier_contact.email)
                    # text_message = strip_tags(html_message)
                    # part1 = MIMEText(text_message, 'plain')
                    # part2 = MIMEText(html_message, 'html')
                    # msg.attach(part1)
                    # msg.attach(part2)
                    #
                    # send_mail(
                    #     'Запрос цены',
                    #     msg.as_string(),
                    #     settings.EMAIL_HOST_USER,
                    #     [supplier_contact.email],
                    #     fail_silently=False,
                    # )
                    plain_text = strip_tags(html_message)
                    msg = EmailMultiAlternatives('Запрос цены', plain_text, settings.EMAIL_HOST_USER, [supplier_contact.email])
                    msg.attach_alternative(html_message, "text/html")
                    msg.send()


            except Exception as e:
                print(str(e))
                return Response({'error': "Не удалось отправить запрос"})

            # try:
            #     order.set_stage(2)
            # except Exception as e:
            #     raise Exception(str(e))

            return Response({'Result': 'Ok'})
        else:
            return Response({'error': "У Вас уже отправлен запрос на этот заказ"})


class MakeOrderAPI(APIView):

    def post(self, request):
        order_id = request.data['order_id']
        order = Order.objects.get(id=order_id)
        if order.order_stage == 2:
            for product in order.products_in_order.all():
                min_price = 0
                best_items = []
                for item in order.items_in_order.all():
                    if item.item.product == product.product:
                        if len(best_items) == 0:
                            min_price = item.price_offer.price_per_unit
                            best_items.append(item)

                        if item.price_offer.price_per_unit < min_price:
                            min_price = item.price_offer.price_per_unit
                            best_items = [item]
                        elif item.price_offer.price_per_unit == min_price:
                            min_price = item.price_offer.price_per_unit
                            best_items.append(item)

                for best in best_items:
                    best.select()


            order.set_stage(3)

        return Response({"Result": 'OK'})

# endregion
