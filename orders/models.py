from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class PriceOffer(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name="price_offers", verbose_name="К товару")
    for_quantity = models.PositiveIntegerField(verbose_name='Для количества товара')
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Цена за единицу')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.item} - {self.price_per_unit}'

    class Meta:
        verbose_name = 'Предложение цены'
        verbose_name_plural = 'Предложения цены'


class Order(models.Model):
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='Создатель')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ItemToOrder(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name="orders", verbose_name="Товар")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items_in_order', verbose_name='Заказ')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price_offer = models.OneToOneField(PriceOffer, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Предложение цены')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.item} в кол-ве {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
