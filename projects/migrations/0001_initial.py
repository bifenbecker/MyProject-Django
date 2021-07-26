# Generated by Django 3.2.4 on 2021-07-26 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.PositiveSmallIntegerField(choices=[(0, 'Создатель'), (1, 'Зритель')], verbose_name='Права доступа')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_in_projects', to=settings.AUTH_USER_MODEL, verbose_name='Участник проетка')),
            ],
            options={
                'verbose_name': 'Участник проекта',
                'verbose_name_plural': 'Участники проекта',
            },
        ),
        migrations.CreateModel(
            name='InviteLinkToProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('member_invite', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_links', to='projects.projectmember', verbose_name='Приглашающий')),
                ('project', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_link', to='projects.project', verbose_name='Проект')),
            ],
        ),
    ]
