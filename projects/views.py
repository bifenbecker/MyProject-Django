from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from orders.models import Stage, Order
from orders.views import get_last_price_by_order
from .models import *

from Pilaru import settings
from projects.forms import *


def is_auth(func):
    """Check is authenticated user"""

    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(self, request, *args, **kwargs)
        else:
            return redirect('login_url')
    return wrapper


class CreateProjectView(View):
    template_name = 'create_project.html'

    @is_auth
    def get(self, request, *args, **kwargs):
        form = CreateProjectForm(request.POST or None)
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Новый проект',
            'toolbar_title': 'Создать новый проект',
            'form': form,
        }
        return render(request, self.template_name, context=context)

    @is_auth
    def post(self, request, *args, **kwargs):
        form = CreateProjectForm(request.POST or None)
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Новый проект',
            'toolbar_title': 'Создать новый проект',
            'form': form,
        }
        if form.is_valid():
            new_project = Project.objects.create(name=form.cleaned_data['name'])
            order = Order.objects.create(created_by=request.user, project=new_project)
            request.user.set_active_order(order)
            ProjectMember.objects.create(user=request.user, access=0, project=new_project)
            return redirect('project_detail_url', project_id=new_project.id)
        return render(request, self.template_name, context=context)


class ProjectDetailView(View):
    template_name = 'project_detail.html'

    @is_auth
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        creator = project.members.all().filter(access=0).first()

        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Проект:' + str(project.id),
            'toolbar_title': project.name,
            'project': project,
            'creator': creator,
            'last_price': get_last_price_by_order(request.user, project.get_active_order()) if project.get_active_order() else None,
            'stages': Stage.objects.all(),
        }
        return render(request, self.template_name, context=context)

    @is_auth
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        creator = project.members.all().filter(access=0).first()

        project_member = request.user.member_in_projects.get(project=project)
        invite_link = InviteLinkToProject(member_invite=project_member, project=project)
        invite_link.save()

        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Проект:' + str(project.id),
            'toolbar_title': project.name,
            'project': project,
            'creator': creator,
            'last_price': get_last_price_by_order(request.user, project.get_active_order()) if project.get_active_order() else None,
            'stages': Stage.objects.all(),
            'invite_link': invite_link,
            'last_price': get_last_price_by_order(request.user,
                                                  project.get_active_order()) if project.get_active_order() else None,
            'stages': Stage.objects.all(),
        }
        return render(request, self.template_name, context=context)


class ProjectListView(View):
    template_name = 'project_list.html'

    @is_auth
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Проекты',
            'toolbar_title': 'Мои проекты',
        }

        try:
            project_list = []
            for project_member in request.user.member_in_projects.all():
                project_list.append(project_member.project)

            context.update({'project_list': project_list})
        except Exception as e:
            context.update({'error': str(e)})

        return render(request, self.template_name, context=context)


# TODO: Fix invite link(need to work last gen link)
class InviteToProjectView(View):
    template_name = 'invite_to_project.html'

    @is_auth
    def get(self, request, link_key):
        invite_link = get_object_or_404(InviteLinkToProject, link_key=link_key)
        context = {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Приглашение',
            'toolbar_title': 'Приглашение в проект',
            'invite_link': invite_link,
        }
        if invite_link.member_invite.user == request.user:
            context.update({'message': 'Вы пытаетесь пригласить себя :)'})
        return render(request, self.template_name, context=context)

    @is_auth
    def post(self, request, link_key):
        try:
            invite_link = get_object_or_404(InviteLinkToProject, link_key=link_key)
            project = invite_link.project
            user = request.user
            for member in project.members.all():
                if member.user == user:
                    return redirect('project_detail_url', project_id=project.id)

            ProjectMember.objects.create(access=1, user=user, project=project)
            return redirect('project_detail_url', project_id=project.id)
        except:
            return redirect('search_url')