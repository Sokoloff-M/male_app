from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FoodItem

@receiver([post_save, post_delete], sender=FoodItem)
def update_meal_totals(sender, instance, **kwargs):
    if instance.meal:
        instance.meal.update_totals()