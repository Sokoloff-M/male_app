from rest_framework import serializers
from .models import Workout, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'sets', 'reps', 'weight')

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'name', 'date', 'duration', 'calories_burned', 'notes', 'exercises')
        read_only_fields = ('user', 'date')