from django.urls import path, include
from .views import *


urlpatterns = [
    path('create-project', CreateProjectView.as_view(), name='create_project_url'),
    path('<int:project_id>', ProjectDetailView.as_view(), name='project_detail_url'),
    path('my-projects', ProjectListView.as_view(), name='project_list_url'),
    path('invite/<uuid:link_key>', InviteToProjectView.as_view(), name='invite_to_project_url'),
]