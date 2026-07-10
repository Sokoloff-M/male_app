from django.utils import timezone
from rest_framework import serializers
from .models import Hobby, HobbyLog


class HobbyLogSerializer(serializers.ModelSerializer):
    hobby_id = serializers.IntegerField(source='hobby.id', read_only=True)

    class Meta:
        model = HobbyLog
        fields = ('id', 'hobby_id', 'date', 'duration_minutes', 'notes', 'created_at')
        read_only_fields = ('date', 'created_at')


class HobbySerializer(serializers.ModelSerializer):
    logs = HobbyLogSerializer(many=True, read_only=True)

    class Meta:
        model = Hobby
        fields = (
            'id', 'name', 'category', 'status', 'priority',
            'notes', 'created_at', 'completed_at', 'logs',
        )
        read_only_fields = ('user', 'created_at', 'completed_at')

    def _update_completed_at(self, instance, status):
        if status == 'completed' and not instance.completed_at:
            instance.completed_at = timezone.now()
        elif status != 'completed':
            instance.completed_at = None

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        self._update_completed_at(instance, status)
        instance.save()
        return instance
