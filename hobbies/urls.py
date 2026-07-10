from django.urls import path
from .views import HobbyListCreateView, HobbyDetailView, HobbyLogListCreateView

app_name = 'hobbies'

urlpatterns = [
    path('', HobbyListCreateView.as_view(), name='list'),
    path('<int:pk>/', HobbyDetailView.as_view(), name='detail'),
    path('<int:hobby_pk>/logs/', HobbyLogListCreateView.as_view(), name='log-list'),
]
