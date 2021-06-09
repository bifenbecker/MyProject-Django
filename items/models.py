from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class ItemCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name="child", verbose_name="Родительская категория")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Item(models.Model):
    UNIT_MEASUREMENT_CHOICES = (
        (0, 'Часов'),
        (1, 'Дней'),
        (2, 'Штуки'),
        (3, 'Раз'),
        (4, 'м'),
        (5, 'м2'),
        (6, 'м3'),
        (7, 'Тонны'),
        (8, 'Килограммы'),
        (9, 'Копмлекты'),
        (10, 'Коробки'),
        (11, 'Упаковки'),
        (12, 'Рулоны'),
        (13, 'Бух'),
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="items", verbose_name="Поставщик")
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, related_name="items", verbose_name="Категория")
    unit_measurement = models.PositiveSmallIntegerField(choices=UNIT_MEASUREMENT_CHOICES, verbose_name='Единица измерения')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
