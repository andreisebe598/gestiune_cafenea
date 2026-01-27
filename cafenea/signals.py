# cafenea/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Client

@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        nume_complet = f"{instance.last_name} {instance.first_name}".strip()
        
        if not nume_complet:
            nume_complet = instance.username

        Client.objects.create(
            user=instance,
            nume=nume_complet,
            gen='Nespecificat' 
        )

@receiver(post_save, sender=User)
def save_client_profile(sender, instance, **kwargs):
    try:
        instance.client.save()
    except Client.DoesNotExist:
        nume_complet = f"{instance.last_name} {instance.first_name}".strip() or instance.username
        Client.objects.create(user=instance, nume=nume_complet)