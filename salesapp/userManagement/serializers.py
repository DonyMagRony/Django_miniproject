from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True},
        }

    def validate_role(self, value):
        # Block 'admin' role from being set at registration unless superuser
        if value == 'admin' and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("You cannot assign the 'admin' role.")
        if value not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            raise serializers.ValidationError(f"Role must be one of: {', '.join([choice[0] for choice in CustomUser.ROLE_CHOICES])}")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user