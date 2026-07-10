from django.db.models import Case, IntegerField, Value, When
from rest_framework import generics, permissions
from .models import Hobby, HobbyLog
from .serializers import HobbySerializer, HobbyLogSerializer


def hobby_priority_order():
    return Case(
        When(priority='high', then=Value(0)),
        When(priority='medium', then=Value(1)),
        When(priority='low', then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )


class HobbyListCreateView(generics.ListCreateAPIView):
    serializer_class = HobbySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            Hobby.objects.filter(user=self.request.user)
            .annotate(priority_order=hobby_priority_order())
            .order_by('priority_order', '-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HobbyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HobbySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Hobby.objects.filter(user=self.request.user)


class HobbyLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HobbyLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        hobby_id = self.kwargs['hobby_pk']
        return HobbyLog.objects.filter(
            hobby__id=hobby_id,
            hobby__user=self.request.user,
        ).order_by('-date', '-created_at')

    def perform_create(self, serializer):
        hobby_id = self.kwargs['hobby_pk']
        hobby = generics.get_object_or_404(Hobby, id=hobby_id, user=self.request.user)
        serializer.save(hobby=hobby)
