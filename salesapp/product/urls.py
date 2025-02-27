from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    # API endpoints under /api/
    path('api/', include(router.urls)),
    # Template-based views
    path('create-category/', TemplateView.as_view(template_name='product/create_category.html'), name='create_category'),
    path('create-product/', TemplateView.as_view(template_name='product/create_product.html'), name='create_product'),
    path('product/', TemplateView.as_view(template_name='product/product_list.html'), name='product_list'),
]