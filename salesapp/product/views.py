from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import TraderOnlyForUnsafe
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from .tasks import process_product_image
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [TraderOnlyForUnsafe]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    renderer_classes = [JSONRenderer]  # Force JSON response, no HTML form

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [TraderOnlyForUnsafe]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'price']
    search_fields = ['name', 'description', 'tags__name']
    ordering_fields = ['price', 'created_at', 'name']
    renderer_classes = [JSONRenderer]  # Force JSON response, no HTML form

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        product = serializer.save()
        process_product_image.delay(product.id)

    def perform_update(self, serializer):
        product = serializer.save()
        if 'image' in self.request.data:
            process_product_image.delay(product.id)