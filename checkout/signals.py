from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineGame


@receiver(post_save, sender=OrderLineGame)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on linegame update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineGame)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on linegame delete
    """
    instance.order.update_total()
