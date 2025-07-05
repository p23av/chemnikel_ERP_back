from rest_framework import serializers

from users.services import send_invitation_email
from .models import User
from .utils import decode_token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'role', 'is_active']
        read_only_fields = ['id', 'role']  # Чтобы нельзя было менять роль через API

class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = User
        fields = ['username', 'full_name', 'role', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_invitation_email(user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CompleteRegistrationSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def save(self):
        
        user_id = decode_token(self.validated_data['token'])
        try:
            user = User.objects.get(id=user_id, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный или просроченный токен")

        user.set_password(self.validated_data['password'])
        user.is_active = True
        user.save()
        return user

class WhoAmISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'role']
