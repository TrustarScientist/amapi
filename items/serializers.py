
from rest_framework import serializers
from .models import Item, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    # Read-only fields to show useful info without extra queries
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Item
        fields = [
            'id', 'seller', 'seller_username', 'category', 'category_name', 
            'title', 'description', 'price', 'is_available', 'created_at'
        ]
        read_only_fields = ['seller']