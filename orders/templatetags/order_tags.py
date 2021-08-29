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
    print(iter, index)
    if iter:
        return iter[index]
    else:
        return "-1"