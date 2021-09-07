from django import template

register = template.Library()


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

def get_last_price(item, user):
    return "-1"

register.filter('get_last_price', get_last_price)