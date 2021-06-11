from django.contrib import admin
from .models import Supplier, ItemCategory, Item, Product

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
    list_display = ["name", "product", 'created_date']
    list_filter = ['product', "created_date"]
    readonly_fields = ("created_date", )
    search_fields = ["name"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "supplier"]
    list_filter = ['category', 'supplier']
    search_fields = ["name", 'supplier', 'category']



admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Product, ProductAdmin)