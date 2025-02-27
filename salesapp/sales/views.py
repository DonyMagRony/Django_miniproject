from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from product.permissions import TraderOnlyForUnsafe
from rest_framework.renderers import JSONRenderer

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, TraderOnlyForUnsafe]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return SalesOrder.objects.all()
        elif user.role == 'seller':
            return SalesOrder.objects.filter(sales_rep=user)
        return SalesOrder.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(sales_rep=self.request.user)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, TraderOnlyForUnsafe]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Invoice.objects.all()
        elif user.role == 'seller':
            return Invoice.objects.filter(order__sales_rep=user)
        return Invoice.objects.filter(order__customer=user)