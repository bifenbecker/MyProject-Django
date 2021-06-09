from django.contrib import admin
from .models import Supplier, ItemCategory, Item

# Register your models here.


class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "created_date"]
    list_filter = ["created_date"]
    readonly_fields = ("created_date", )
    search_fields = ["name"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", 'parent', "created_date"]
    list_filter = ["created_date", 'parent']
    readonly_fields = ("created_date", )
    search_fields = ["name"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "category", 'supplier', 'created_date']
    list_filter = ['category', 'supplier', "created_date"]
    readonly_fields = ("created_date", )
    search_fields = ["name", 'supplier']
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Item, ItemAdmin)
