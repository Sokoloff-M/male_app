from rest_framework import generics, permissions
from .models import Meal, FoodItem
from .serializers import MealSerializer, FoodItemSerializer

class MealListCreateView(generics.ListCreateAPIView):
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MealDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

class FoodItemListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        meal_id = self.kwargs['meal_pk']
        return FoodItem.objects.filter(meal__id=meal_id, meal__user=self.request.user)

    def perform_create(self, serializer):
        meal_id = self.kwargs['meal_pk']
        meal = generics.get_object_or_404(Meal, id=meal_id, user=self.request.user)
        serializer.save(meal=meal)

class FoodItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return FoodItem.objects.filter(meal__user=self.request.user)