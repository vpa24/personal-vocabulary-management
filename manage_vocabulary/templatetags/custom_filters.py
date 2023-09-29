from django import template
import calendar

register = template.Library()


@register.filter
def replacetoSpace(value):
    return value.replace('-', ' ')


@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]


@register.filter
def add_if_plural(value):
    return f'{value} words' if value > 1 else f'{value} word'
