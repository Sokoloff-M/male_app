from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'weight', 'height', 'gender', 'goal', 'avatar')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'age', 'weight', 'height', 'gender', 'goal')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        user.age = validated_data.get('age')
        user.weight = validated_data.get('weight')
        user.height = validated_data.get('height')
        user.gender = validated_data.get('gender', 'M')
        user.goal = validated_data.get('goal', '')
        user.save()
        return user