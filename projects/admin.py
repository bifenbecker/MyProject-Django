from django.contrib import admin

from projects.models import *


class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ["user", "access"]
    list_filter = ["user"]
    search_fields = ["user"]
    ordering = ["-user"]


class ProjectAdmin(admin.ModelAdmin):
    fields = ['name', 'created_date']
    list_display = ('name', 'created_date')
    list_filter = ["created_date"]
    readonly_fields = ("created_date",)
    search_fields = ["name"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


admin.site.register(ProjectMember, ProjectMemberAdmin)
# admin.site.register(Project, ProjectAdmin)