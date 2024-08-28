from base.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = '__all__'


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


