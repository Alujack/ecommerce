from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name',
                  'phone_number', 'role',
                  'image'
                  ]
        read_only_fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.update_or_create(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token




class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerList
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = '__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = '__all__'


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class PromotionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCategory
        fields = '__all__'


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class ShopOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOrder
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'
