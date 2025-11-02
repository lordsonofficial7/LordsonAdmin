from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet, ProductViewSet, OrderViewSet  # 👈 also include ProductViewSet if you have it

# Create a router and register your API endpoints
router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
