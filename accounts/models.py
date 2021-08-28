from django.db import models
from django.contrib.auth.models import AbstractUser
from orders.models import Order, OrderStateToOrder, OrderState
from django.core.exceptions import ObjectDoesNotExist

from projects.models import Project



class User(AbstractUser):

    active_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, verbose_name='Активный заказ', null=True, default=None)

    def get_active_order(self):
        order_state_to_order = OrderStateToOrder.objects.filter(order__created_by=self, state=OrderState.objects.get(name='Активный'), finished_date__isnull=True).first()
        return order_state_to_order.order if order_state_to_order else None

    def get_active_project(self):
        if self.member_in_projects.all().last() is not None:
            return self.member_in_projects.all().last().project
        else:
            return None

    def get_active_orders_from_projects(self):
        projects = self.member_in_projects.all()
        res = 0
        for project in projects:
            if project.project.get_active_order():
                res += 1

        return res

    def set_active_order(self, order: Order):
        self.active_order = order
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


