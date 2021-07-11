from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


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


class OrderState(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders', verbose_name='Создатель')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def get_order_state(self):
        return self.order_states.filter(finished_date__isnull=True).first()

    def set_order_state(self, new_order_state: OrderState):
        order_state_to_order = self.get_order_state()
        if order_state_to_order:
            order_state_to_order.finished_date = datetime.now()
            order_state_to_order.save()
        OrderStateToOrder.objects.create(order=self, state=new_order_state)

    def __str__(self):
        return str(self.created_by)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderStateToOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_states', verbose_name='Заказ')
    state = models.ForeignKey(OrderState, on_delete=models.PROTECT, related_name='+', null=True, blank=True, verbose_name='Статус заказа')
    finished_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата завершения")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.order} - {self.state}'

    class Meta:
        verbose_name = 'Статус заказа к заказу'
        verbose_name_plural = 'Статус заказы к заказам'


class Stage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name="child", verbose_name="Родительский этап")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'


class ItemToOrder(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name="orders", verbose_name="Товар")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items_in_order', verbose_name='Заказ')
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name='+', null=True, blank=True, verbose_name='Этап')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price_offer = models.OneToOneField(PriceOffer, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Предложение цены')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.item} в кол-ве {self.quantity}'

    def get_total_price(self):
        if self.price_offer:
            return self.quantity * self.price_offer.price_per_unit
        else:
            return None

    class Meta:
        ordering = ['id']
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
