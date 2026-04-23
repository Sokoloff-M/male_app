from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django.core.validators import MinValueValidator

class Meal(models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, verbose_name='Тип приёма пищи')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    total_calories = models.PositiveIntegerField(verbose_name='Калории', default=0)
    total_proteins = models.PositiveIntegerField(verbose_name='Белки (г)', default=0)
    total_fats = models.PositiveIntegerField(verbose_name='Жиры (г)', default=0)
    total_carbs = models.PositiveIntegerField(verbose_name='Углеводы (г)', default=0)
    notes = models.TextField(blank=True, verbose_name='Заметки')
    
    def update_totals(self):
        """Пересчитать суммарные калории и БЖУ из всех FoodItem этого приёма пищи."""
        agg = self.food_items.aggregate(
            total_calories=Sum(F('calories') * F('quantity')),
            total_proteins=Sum(F('proteins') * F('quantity')),
            total_fats=Sum(F('fats') * F('quantity')),
            total_carbs=Sum(F('carbs') * F('quantity')),
        )
        self.total_calories = agg['total_calories'] or 0
        self.total_proteins = agg['total_proteins'] or 0
        self.total_fats = agg['total_fats'] or 0
        self.total_carbs = agg['total_carbs'] or 0
        self.save(update_fields=['total_calories', 'total_proteins', 'total_fats', 'total_carbs'])

    class Meta:
        verbose_name = 'Приём пищи'
        verbose_name_plural = 'Приёмы пищи'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.get_meal_type_display()} - {self.date}"

class FoodItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=200, verbose_name='Продукт')
    calories = models.PositiveIntegerField(verbose_name='Калории', validators=[MinValueValidator(0)])
    proteins = models.PositiveIntegerField(verbose_name='Белки', validators=[MinValueValidator(0)])
    fats = models.PositiveIntegerField(verbose_name='Жиры', validators=[MinValueValidator(0)])
    carbs = models.PositiveIntegerField(verbose_name='Углеводы', validators=[MinValueValidator(0)])
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, default=1,
        validators=[MinValueValidator(0.01)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} x{self.quantity}"