from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.Truck)
def auto_create_truck_relations(sender, instance, **kwargs):
    if kwargs.get('created'):
        models.Cargo.objects.get_or_create(truck=instance)
