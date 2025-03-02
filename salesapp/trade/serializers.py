from rest_framework import serializers
from .models import Order, Transaction
from product.serializers import ProductSerializer
from userManagement.serializers import UserSerializer
from product.models import Product

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'executed_price', 'executed_quantity', 'executed_at', 'transaction_fee']
        read_only_fields = ['executed_at']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_id', 'order_type', 'quantity', 'price', 'status', 'created_at',
                  'updated_at', 'transactions']
        read_only_fields = ['user', 'created_at', 'updated_at']