from rest_framework import generics, permissions
from .models import Workout
from .serializers import WorkoutSerializer
from .serializers import WorkoutSerializer, ExerciseSerializer
from .models import Workout, Exercise

class WorkoutListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)
class ExerciseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Фильтруем упражнения по тренировке, переданной в URL
        workout_id = self.kwargs['workout_pk']
        return Exercise.objects.filter(workout__id=workout_id, workout__user=self.request.user)

    def perform_create(self, serializer):
        workout_id = self.kwargs['workout_pk']
        workout = generics.get_object_or_404(Workout, id=workout_id, user=self.request.user)
        serializer.save(workout=workout)

class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Exercise.objects.filter(workout__user=self.request.user)