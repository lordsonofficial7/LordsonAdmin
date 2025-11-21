from rest_framework import serializers
from .models import Banner, Product, Order, ProductImage


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        try:
            return obj.image.url if obj.image else None
        except Exception:
            # Prevent crashes if S3 is not reachable or image is missing
            return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'discount',
            'category', 'sizes', 'image_url', 'final_price', 'created_at', 'images'
        ]

    def get_image_url(self, obj):
        try:
            return obj.image.url if obj.image else None
        except Exception:
            return None


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"