from urllib.parse import urlencode

from django.db import models
import random, time

from django.utils.timezone import now


class ProjectMember(models.Model):
    ACCESS_RIGHTS = (
        (0, 'Создатель'),
        (1, 'Зритель'),
    )
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='member_in_projects', verbose_name='Участник проетка')
    access = models.PositiveSmallIntegerField(choices=ACCESS_RIGHTS, verbose_name='Права доступа')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        if self.user.username == self.user.email:
            return self.user.username.split("@")[0]
        else:
            return self.user.username

    class Meta:
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'


class InviteLinkToProject(models.Model):
    member_invite = models.ForeignKey('ProjectMember', on_delete=models.CASCADE, related_name='invite_links', verbose_name='Приглашающий', default=None, null=True)
    link = models.CharField(max_length=356, unique=True, verbose_name='Ссылка для приглашения в проект')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.CharField(max_length=50, unique=True, verbose_name='Slug')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект', related_name='invite_link', default=None, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
        self.generate_link()


    def generate_slug(self):
        import time
        id = self.project.id
        time = int(time.time())
        rand = int(random.random() * 1000)
        try:
            self.slug = str(id) + str(time) + str(rand)
        except:
            self.slug = str(id) + str(time) + str(rand + 1)

    def generate_link(self):
        # TODO: Need to change host
        BASE = "localhost:8000/project/invite/?"
        data = {
            'member_invite_id': self.member_invite.id,
            'member_invite': self.member_invite,
            'project_name': self.project.name,
            'project_id': self.project.id,
            'slug': self.slug,
        }
        data_url_encode = urlencode(data)
        self.link = BASE + data_url_encode

    def __str__(self):
        return self.link


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_active_order(self):
        if self.orders_in_project.all().last() is not None:
            return self.orders_in_project.all().last()
        else:
            return None

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
