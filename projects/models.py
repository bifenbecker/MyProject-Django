from django.db import models
from django.conf import settings
import uuid


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
    link_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    member_invite = models.ForeignKey('ProjectMember', on_delete=models.CASCADE, related_name='invite_links', verbose_name='Приглашающий', default=None, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект', related_name='invite_link', default=None, null=True)

    @property
    def link(self):
        return settings.URL_BASE + "/project/invite/" + str(self.link_key)

    def __str__(self):
        return self.link_key


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_active_order(self):
        return self.orders_in_project.all().last()

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
