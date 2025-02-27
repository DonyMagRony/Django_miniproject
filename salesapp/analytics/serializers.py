# myapp/serializers.py
from rest_framework import serializers
from product.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, 
        slug_field='name', 
        queryset=None,  
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
