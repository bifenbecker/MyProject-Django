# Generated by Django 3.2.4 on 2021-06-14 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='itemtoorder',
            name='stage',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='orders.stage', verbose_name='Этап'),
            preserve_default=False,
        ),
    ]
