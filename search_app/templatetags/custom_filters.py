from django import template

register = template.Library()

@register.filter
def to(value):
    try:
        return range(1, value + 1)
    except TypeError:
        return []
