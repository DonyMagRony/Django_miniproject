from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from profileManagement.tasks import create_user_profile, save_user_profile

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Obtain a pair of JWT tokens (access and refresh)",
        request_body=CustomTokenObtainPairSerializer,
        responses={
            200: openapi.Response(
                description="JWT Tokens",
                examples={"application/json": {"access": "your-access-token", "refresh": "your-refresh-token"}}
            ),
            400: openapi.Response(
                description="Validation Error",
                examples={"application/json": {"detail": "Invalid credentials"}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user with role selection (trader, seller, customer)",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: openapi.Response(
                description="Validation Error",
                examples={"application/json": {"detail": "Invalid role or username already exists"}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES if choice[0] != 'admin']
        if role not in valid_roles:
            raise ValidationError({'role': f'Role must be one of: {", ".join(valid_roles)}'})
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        create_user_profile.delay(user.id)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            save_user_profile.delay(user.id)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html', {'title': 'Login'})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if not username or not password or not role:
            messages.error(request, 'Please fill out all fields, including role.')
        else:
            valid_roles = [choice[0] for choice in User.ROLE_CHOICES if choice[0] != 'admin']
            if role not in valid_roles:
                messages.error(request, f'Invalid role selected. Choose from: {", ".join(valid_roles)}')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                else:
                    user = User.objects.create_user(username=username, password=password, role=role)
                    create_user_profile.delay(user.id)
                    messages.success(request, 'Registered successfully!')
                    return redirect('login')
    return render(request, 'users/register.html', {'title': 'Register'})