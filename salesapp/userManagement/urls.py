from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TemplateView.as_view(template_name='users/login.html'), name='login'),
]