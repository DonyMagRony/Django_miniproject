from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import re_path


router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]
