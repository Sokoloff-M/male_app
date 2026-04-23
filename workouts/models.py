from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=200, verbose_name='Название тренировки')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    duration = models.PositiveIntegerField(verbose_name='Длительность (мин)', validators=[MinValueValidator(1)])
    calories_burned = models.PositiveIntegerField(verbose_name='Сожжено калорий', default=0, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.date}"

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=200, verbose_name='Упражнение')
    sets = models.PositiveIntegerField(verbose_name='Подходы', validators=[MinValueValidator(1)])
    reps = models.PositiveIntegerField(verbose_name='Повторения', validators=[MinValueValidator(1)])
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Вес (кг)', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return f"{self.name} - {self.sets}x{self.reps}"