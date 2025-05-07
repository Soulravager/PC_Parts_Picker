# parts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

##FOR RATING UPDATE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import UserRating, CPU, GPU, Motherboard, RAM, SSD, PSU

@receiver(post_save, sender=UserRating)
def update_part_rating_on_save(sender, instance, **kwargs):
    """Automatically update part's rating when a new rating is added."""

    model_mapping = {
        "cpu": CPU,
        "gpu": GPU,
        "motherboard": Motherboard,
        "ram": RAM,
        "ssd": SSD,
        "psu": PSU,
    }

    part_model_name = instance.part_model  # Get model name (e.g., "Ryzen 7 5800X")
    category = instance.category.lower() if instance.category else None  # Get category

    if category in model_mapping:
        model_class = model_mapping[category]

        try:
            part = model_class.objects.get(model=part_model_name)  # Find matching part
            avg_rating = UserRating.objects.filter(part_model=part_model_name).aggregate(Avg("rating"))["rating__avg"]
            part.rating = round(avg_rating or 1)
            part.save(update_fields=["rating"])  # Update only 'rating' field
        except model_class.DoesNotExist:
            pass  # Ignore if no matching part is found
