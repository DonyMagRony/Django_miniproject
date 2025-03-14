from rest_framework import serializers
from .models import SalesOrder, OrderItem, Invoice
from product.serializers import ProductSerializer
from userManagement.serializers import UserSerializer
from product.models import Product
from userManagement.models import CustomUser
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=2147483647  # Max for PositiveIntegerField
    )
    subtotal = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True  # Add this
    )
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['order', 'price']  # Price is read-only

    def create(self, validated_data):
        # Auto-set price from product
        product = validated_data['product']
        validated_data['price'] = product.price
        return super().create(validated_data)

    def validate(self, data):
        if 'price' not in data:
            data['price'] = data['product'].price
        return data

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'pdf_file', 'total_amount', 'generated_at', 'due_date', 'paid']
        read_only_fields = ['order', 'generated_at', 'total_amount']

class SalesOrderSerializer(serializers.ModelSerializer):
    sales_rep = UserSerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='customer',
        write_only=True
    )
    items = OrderItemSerializer(many=True, source='orderitem_set')
    invoice = InvoiceSerializer(read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'sales_rep', 'customer', 'customer_id', 'items', 'discount',
            'status', 'created_at', 'updated_at', 'invoice', 'total'
        ]
        read_only_fields = ['sales_rep', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('orderitem_set')
        order = SalesOrder.objects.create(**validated_data)  # Removed sales_rep here
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('orderitem_set', None)
        instance = super().update(instance, validated_data)
        if items_data:
            instance.orderitem_set.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance