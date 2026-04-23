from django.urls import path
from .views import WorkoutListCreateView, WorkoutDetailView, ExerciseListCreateView, ExerciseDetailView

app_name = 'workouts'

urlpatterns = [
    path('', WorkoutListCreateView.as_view(), name='list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='detail'),
    path('<int:workout_pk>/exercises/', ExerciseListCreateView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
]