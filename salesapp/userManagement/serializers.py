from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True},  # Make role mandatory
        }

    def validate_role(self, value):
        # Block the "admin" role from being set at registration
        if value == 'admin':
            raise serializers.ValidationError("You cannot assign the 'admin' role.")
        return value

    def create(self, validated_data):
        # Create user with validated data
        user = CustomUser.objects.create_user(**validated_data)
        return user