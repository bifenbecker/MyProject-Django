# Generated by Django 3.2.4 on 2021-07-26 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('slug', models.SlugField(default=None, max_length=200, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='items.itemcategory', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('unit_measurement', models.PositiveSmallIntegerField(choices=[(0, 'Часов'), (1, 'Дней'), (2, 'Штуки'), (3, 'Раз'), (4, 'м'), (5, 'м2'), (6, 'м3'), (7, 'Тонны'), (8, 'Килограммы'), (9, 'Копмлекты'), (10, 'Коробки'), (11, 'Упаковки'), (12, 'Рулоны'), (13, 'Бух')], verbose_name='Единица измерения')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.itemcategory', verbose_name='Категория продукта')),
                ('similar', models.ManyToManyField(related_name='_items_product_similar_+', to='items.Product', verbose_name='Аналоги')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=None, max_length=200, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('unit_measurement', models.PositiveSmallIntegerField(choices=[(0, 'Часов'), (1, 'Дней'), (2, 'Штуки'), (3, 'Раз'), (4, 'м'), (5, 'м2'), (6, 'м3'), (7, 'Тонны'), (8, 'Килограммы'), (9, 'Копмлекты'), (10, 'Коробки'), (11, 'Упаковки'), (12, 'Рулоны'), (13, 'Бух')], verbose_name='Единица измерения')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='items.product', verbose_name='Продукт')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suplliers', to='items.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
