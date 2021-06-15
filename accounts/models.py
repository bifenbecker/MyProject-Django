from django.db import models
from django.contrib.auth.models import AbstractUser
from orders.models import Order, OrderStateToOrder, OrderState


class User(AbstractUser):

    def get_active_order(self):
        order_state_to_order = OrderStateToOrder.objects.filter(order__created_by=self, state=OrderState.objects.get(name='Активный'), finished_date__isnull=True).first()
        return order_state_to_order.order if order_state_to_order else None

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


