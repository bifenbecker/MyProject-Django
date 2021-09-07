from django import template
from items.models import Item
from orders.models import ItemToOrder

register = template.Library()

@register.filter
def get_type(value):
    return type(value)


@register.filter
def get_item(dictionary, key):
    if dictionary and key:
        return dictionary.get(key)
    else:
        return "-1"

@register.filter
def index(iter, index):
    if iter:
        return iter[index]
    else:
        return "-1"

@register.filter
def get_last_price(item, user):
    try:
        if len(user.orders.all().order_by('-created_date').exclude(order_stage=1)) == 0:
            return "У Вас пока нет истории заказов :("

        for order in user.orders.all().order_by('-created_date').exclude(order_stage=1):
            if not order.is_active():
                for item_in_order in order.items_in_order.all():
                    if isinstance(item, ItemToOrder):
                        if item_in_order.item.supplier.name == item.item.supplier.name and item_in_order.item.name == item.item.name:
                            return float(item_in_order.price_offer.price_per_unit)
                    elif isinstance(item, Item):
                        if item_in_order.item.supplier.name == item.supplier.name and item_in_order.item.name == item.name:
                            return float(item_in_order.price_offer.price_per_unit)
        return "Такого товара не было ранее"
    except:
        return "-1"

