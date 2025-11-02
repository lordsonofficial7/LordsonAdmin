from rest_framework import serializers
from .models import Banner, Product, ProductImage, Order


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'discount',
            'category', 'sizes', 'image', 'final_price', 'created_at', 'images'
        ]




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"