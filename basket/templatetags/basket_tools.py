from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    A filter to calculate subtotal in basket
    """
    return price * quantity
