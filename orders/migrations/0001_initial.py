# Generated by Django 3.2.4 on 2021-07-26 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_in_project', to='projects.project')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус заказа',
                'verbose_name_plural': 'Статусы заказа',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='orders.stage', verbose_name='Родительский этап')),
            ],
            options={
                'verbose_name': 'Этап',
                'verbose_name_plural': 'Этапы',
            },
        ),
        migrations.CreateModel(
            name='PriceOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_quantity', models.PositiveIntegerField(verbose_name='Для количества товара')),
                ('price_per_unit', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Цена за единицу')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_offers', to='items.item', verbose_name='К товару')),
            ],
            options={
                'verbose_name': 'Предложение цены',
                'verbose_name_plural': 'Предложения цены',
            },
        ),
        migrations.CreateModel(
            name='OrderStateToOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_states', to='orders.order', verbose_name='Заказ')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='orders.orderstate', verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Статус заказа к заказу',
                'verbose_name_plural': 'Статус заказы к заказам',
            },
        ),
        migrations.CreateModel(
            name='ItemToOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='items.item', verbose_name='Товар')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_in_order', to='orders.order', verbose_name='Заказ')),
                ('price_offer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='orders.priceoffer', verbose_name='Предложение цены')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='orders.stage', verbose_name='Этап')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
                'ordering': ['id'],
            },
        ),
    ]
