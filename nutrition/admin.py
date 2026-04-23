from django.contrib import admin
from .models import Meal, FoodItem

class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 1

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'date', 'total_calories')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'date'
    inlines = [FoodItemInline]

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('meal', 'name', 'calories', 'quantity')
    list_filter = ('meal__meal_type',)
    search_fields = ('name',)