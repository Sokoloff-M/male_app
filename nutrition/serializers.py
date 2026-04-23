# nutrition/serializers.py

from rest_framework import serializers
from .models import Meal, FoodItem

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'calories', 'proteins', 'fats', 'carbs', 'quantity')

class MealSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True, required=False)

    class Meta:
        model = Meal
        fields = ('id', 'meal_type', 'date', 'total_calories', 'total_proteins',
                  'total_fats', 'total_carbs', 'notes', 'food_items')
        read_only_fields = ('user', 'date', 'total_calories', 'total_proteins',
                            'total_fats', 'total_carbs')  # totals теперь только для чтения

    def create(self, validated_data):
        food_items_data = validated_data.pop('food_items', [])
        meal = Meal.objects.create(**validated_data)
        for food_data in food_items_data:
            FoodItem.objects.create(meal=meal, **food_data)
        meal.update_totals()  # принудительный пересчёт после добавления всех продуктов
        return meal

    def update(self, instance, validated_data):
        food_items_data = validated_data.pop('food_items', None)
        # Обновляем поля самого Meal
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if food_items_data is not None:
            # Здесь можно реализовать полную замену списка продуктов (сначала удалить старые, потом создать новые)
            instance.food_items.all().delete()
            for food_data in food_items_data:
                FoodItem.objects.create(meal=instance, **food_data)
        instance.update_totals()
        return instance