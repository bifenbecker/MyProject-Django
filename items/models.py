from django.db import models
from django.utils.text import slugify
from time import time
import random


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
    slug = models.SlugField(max_length=200, unique=True, default=None)

    def _generate_slug(self):
        parent_slug = self.parent._generate_slug() + '--' if self.parent else ''
        return parent_slug + slugify(self.name, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self._generate_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    category = models.ForeignKey(ItemCategory, verbose_name="Категория продукта", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


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
    slug = models.SlugField(max_length=200, unique=True, default=None)
    name = models.CharField(max_length=200, verbose_name="Название")
    supplier = models.ForeignKey(Supplier, verbose_name="Поставщик",related_name='suplliers', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name="Продукт", related_name='items', default=None, on_delete=models.CASCADE)
    unit_measurement = models.PositiveSmallIntegerField(choices=UNIT_MEASUREMENT_CHOICES, verbose_name='Единица измерения')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True) + '-' + str(int(time()) + random.random())
        super(Item, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
