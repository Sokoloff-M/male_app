from django.contrib import admin
from .models import Workout, Exercise

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'date', 'duration', 'calories_burned')  # добавил id, duration
    list_filter = ('date', 'user')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'date'

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout', 'name', 'sets', 'reps', 'weight')
    list_filter = ('workout__date',)
    search_fields = ('name',) 