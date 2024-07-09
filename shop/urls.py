from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import product_list, product_detail, ProductViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('', include(router.urls)),
]