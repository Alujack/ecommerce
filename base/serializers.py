from rest_framework import serializers
from .models import User, Seller, Store, Product, ShoppingCart, ShoppingCartItem, ShopOrder, OrderLine, UserPaymentMethod

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password_hash', 'first_name', 'last_name', 'phone_number', 'image']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'user', 'store_name']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'seller', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'store', 'category', 'name', 'description', 'product_image', 'price']

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'cart', 'product_item', 'qty']

class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'items']

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['id', 'product_item', 'order', 'quantity', 'price']

class ShopOrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = ShopOrder
        fields = ['id', 'user', 'order_date', 'payment_method', 'shipping_address', 'shipping_method', 'order_total', 'order_status', 'order_lines']

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethod
        fields = ['id', 'user', 'payment_type', 'provider', 'card_number', 'expiry_date']
