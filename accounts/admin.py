from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username"]
    list_filter = ["email"]
    search_fields = ["email"]


admin.site.register(User, UserAdmin)

