from .models import Product, Cart, CartItem, PaymentMethod, Order
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, PaymentMethodSerializer, OrderSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response  
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .paypal import create_paypal_payment

@api_view(['GET'])

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()
        return Response({'status': 'item added'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        product = Product.objects.get(pk=product_id)
        CartItem.objects.filter(cart=cart, product=product).delete()
      
        return Response({'status': 'item removed'}, status=status.HTTP_200_OK)

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        cart = Cart.objects.get(pk=self.request.data.get('cart_id'))
        payment_method = PaymentMethod.objects.get(pk=self.request.data.get('payment_method_id'))
        serializer.save(user=self.request.user, cart=cart, payment_method=payment_method)
        return super().perform_create(serializer)
    
    @action(detail=True, methods=['post'])
    def create_paypal_payment(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        payment_url = create_paypal_payment(cart)
        if payment_url:
            return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'payment creation failed'}, status=status.HTTP_400_BAD_REQUEST)