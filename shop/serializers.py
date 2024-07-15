from rest_framework import serializers
from shop.models import Product, Order, CartItem, Cart, PaymentMethod


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Cart
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    cart = CartSerializer()
    payment_method = PaymentMethodSerializer()
    
    class Meta:
        model = Order
        fields = '__all__'
        