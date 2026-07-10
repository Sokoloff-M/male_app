# pylint: disable=no-member
from django.db import models
from django.conf import settings

class Hobby(models.Model):
    CATEGORY_CHOICES = [
        ('book', 'Книга'),
        ('movie', 'Фильм'),
        ('game', 'Игра'),
        ('sport', 'Спорт'),
        ('other', 'Другое'),
    ]
    STATUS_CHOICES = [
        ('plan', 'В планах'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hobbies')
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='plan')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HobbyLog(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    duration_minutes = models.PositiveIntegerField(
        default=0, verbose_name='Длительность (мин)'
    )
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Лог хобби'
        verbose_name_plural = 'Логи хобби'

    def __str__(self):
        return f"{self.hobby.name} - {self.date}"