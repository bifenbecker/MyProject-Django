from django.db import models
from django.contrib.auth.models import AbstractUser
from orders.models import Order


class User(AbstractUser):
    active_order = models.OneToOneField(Order,related_name='active_order', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


