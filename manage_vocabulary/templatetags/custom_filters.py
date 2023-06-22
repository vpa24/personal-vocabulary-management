from django import template

register = template.Library()

@register.filter
def replacetoSpace(value):
    return value.replace('-', ' ')
