from django.urls import path
from .views import MealListCreateView, MealDetailView, FoodItemListCreateView, FoodItemDetailView

app_name = 'nutrition'

urlpatterns = [
    path('', MealListCreateView.as_view(), name='meal-list'),
    path('<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('<int:meal_pk>/fooditems/', FoodItemListCreateView.as_view(), name='fooditem-list'),
    path('fooditems/<int:pk>/', FoodItemDetailView.as_view(), name='fooditem-detail'),
]