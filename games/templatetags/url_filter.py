from django import template

register = template.Library()


@register.filter
def href_fix(value):
    """
    A filter to add filler to empty spaces where needed in urls
    """
    return value.replace(' ', '%20')
