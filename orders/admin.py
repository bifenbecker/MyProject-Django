from django.contrib import admin
from .models import PriceOffer, Order, ItemToOrder

# Register your models here.


class PriceOfferAdmin(admin.ModelAdmin):
    list_display = ["item", 'for_quantity', 'price_per_unit', "created_date"]
    list_filter = ["created_date"]
    readonly_fields = ('item', 'for_quantity', 'price_per_unit', "created_date", )
    search_fields = ["item"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "created_by", 'created_date']
    list_filter = ["created_date"]
    readonly_fields = ('created_by', "created_date", )
    search_fields = ["created_by"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class ItemToOrderAdmin(admin.ModelAdmin):
    list_display = ["item", "order", 'quantity', 'created_date']
    list_filter = ["created_date"]
    readonly_fields = ('order', "created_date", )
    search_fields = ["item"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


admin.site.register(PriceOffer, PriceOfferAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemToOrder, ItemToOrderAdmin)
