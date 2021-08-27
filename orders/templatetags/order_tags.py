from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(iter, index):
    if iter:
        return iter[index]
    else:
        return "1"