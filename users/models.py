from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Расширенная модель пользователя"""
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    )
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Возраст')
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес (кг)')
    height = models.FloatField(null=True, blank=True, verbose_name='Рост (см)')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')
    goal = models.TextField(blank=True, verbose_name='Цель тренировок')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username