# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()  # Get the custom user model

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description="Obtain a pair of JWT tokens (access and refresh)",
        request=CustomTokenObtainPairSerializer,
        responses={
            200: {
                "description": "JWT Tokens",
                "content": {
                    "application/json": {
                        "example": {
                            "access": "your-access-token",
                            "refresh": "your-refresh-token"
                        }
                    }
                }
            },
            400: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Invalid credentials"
                        }
                    }
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name="username",
                type=OpenApiTypes.STR,
                location="form",
                description="Username of the user"
            ),
            OpenApiParameter(
                name="password",
                type=OpenApiTypes.STR,
                location="form",
                description="Password of the user"
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description="Register a new user with role selection (HR or Seeker)",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: {
                "description": "Validation Error", 
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Invalid role or username already exists"
                        }
                    }
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                location="form",
                description="Email of the new user"
            ),
            OpenApiParameter(
                name="username",
                type=OpenApiTypes.STR,
                location="form",
                description="Username of the new user"
            ),
            OpenApiParameter(
                name="password",
                type=OpenApiTypes.STR,
                location="form",
                description="Password for the new user"
            ),
            OpenApiParameter(
                name="role",
                type=OpenApiTypes.STR,
                location="form",
                description="Role of the new user: 'seeker' or 'hr'"
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        if role not in ['seeker', 'hr']:
            raise ValidationError({'role': 'Role must be either "seeker" or "hr"'})
        return super().post(request, *args, **kwargs)
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html', {'title': 'Login'})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get role from form

        if not username or not password or not role:
            messages.error(request, 'Please fill out all fields, including role.')
        else:
            if role not in ['seeker', 'hr']:
                messages.error(request, 'Invalid role selected.')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                else:
                    User.objects.create_user(username=username, password=password, role=role)
                    messages.success(request, 'Registered successfully!')
                    return redirect('login')

    return render(request, 'users/register.html', {'title': 'Register'})