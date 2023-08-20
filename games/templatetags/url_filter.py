from django import template

register = template.Library()


@register.filter
def href_fix(value):
    return value.replace(' ', '%20')
