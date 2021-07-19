from django.contrib import admin
from .models import PriceOffer, OrderState, Order, OrderStateToOrder, Stage, ItemToOrder

# Register your models here.


class PriceOfferAdmin(admin.ModelAdmin):
    list_display = ["item", 'for_quantity', 'price_per_unit', "created_date"]
    list_filter = ["created_date"]
    readonly_fields = ('item', 'for_quantity', 'price_per_unit', "created_date", )
    search_fields = ["item"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class OrderStateAdmin(admin.ModelAdmin):
    list_display = ['id', "name"]
    search_fields = ["name"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', "created_by", 'created_date', 'project']
    list_filter = ["created_date"]
    readonly_fields = ('created_by', "created_date", )
    search_fields = ["created_by"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class OrderStateToOrderAdmin(admin.ModelAdmin):
    list_display = ['order', "state", 'finished_date', 'created_date']
    list_filter = ["state", 'created_date']
    readonly_fields = ("created_date", )
    search_fields = ["order"]
    date_hierarchy = "created_date"
    ordering = ["-created_date"]


class StageAdmin(admin.ModelAdmin):
    list_display = ['id', "name", 'parent', 'created_date']
    list_filter = ["parent", 'created_date']
    readonly_fields = ("created_date", )
    search_fields = ["name"]
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
admin.site.register(OrderState, OrderStateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStateToOrder, OrderStateToOrderAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(ItemToOrder, ItemToOrderAdmin)
