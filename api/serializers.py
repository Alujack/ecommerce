from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import (
    User, Stock, Store, CustomerList, Address, ProductCategory, Product, ProductItem, Variation,
    VariationOption, ProductConfiguration, Promotion, PromotionCategory, OrderLine, ShoppingCartItem,
    PaymentType, UserPaymentMethod, UserReview, ShopOrder, OrderHistory, ShippingMethod, Favourite, Draft, Publish
)
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


class StockSerializer(serializers.ModelSerializer):
    # or use ProductSerializer() if you need nested data
    product = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Address
        fields = '__all__'

# stroe management


class StoreSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    # stock = StockSerializer()
    address = AddressSerializer()

    class Meta:
        model = Store
        fields = ['seller', 'name', 'address']

    # def create(self, validated_data):
    #     seller_data = validated_data.pop('seller')
    #     # stock_data = validated_data.pop('stock')
    #     address_data = validated_data.pop('address')

    #     # Check if the user with the given email already exists
    #     email = seller_data.get('email')
    #     seller = User.objects.filter(email=email).first()
    #     if not seller:
    #         seller = User.objects.create(**seller_data)
    #     else:
    #         for attr, value in seller_data.items():
    #             setattr(seller, attr, value)
    #         seller.save()

    #     # stock = Stock.objects.create(**stock_data)
    #     address = Address.objects.create(**address_data)

    #     store = Store.objects.create(
    #         seller=seller, address=address, **validated_data)
    #     return store

    # def update(self, instance, validated_data):
    #     seller_data = validated_data.pop('seller', None)
    #     # stock_data = validated_data.pop('stock', None)
    #     address_data = validated_data.pop('address', None)

    #     if seller_data:
    #         email = seller_data.get('email')
    #         seller = User.objects.filter(email=email).first()
    #         if not seller:
    #             seller = User.objects.create(**seller_data)
    #         else:
    #             for attr, value in seller_data.items():
    #                 setattr(seller, attr, value)
    #             seller.save()
    #         instance.seller = seller

    #     # if stock_data:
    #     #     for attr, value in stock_data.items():
    #     #         setattr(instance.stock, attr, value)
    #     #     instance.stock.save()

    #     if address_data:
    #         for attr, value in address_data.items():
    #             setattr(instance.address, attr, value)
    #         instance.address.save()

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     return instance


class CustomerListSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    user = UserSerializer()

    class Meta:
        model = CustomerList
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.StringRelatedField()

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Variation
        fields = '__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    variation = VariationSerializer()

    class Meta:
        model = VariationOption
        fields = '__all__'


class ProductItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variations = VariationOptionSerializer(many=True)

    class Meta:
        model = ProductItem
        fields = '__all__'


class ProductConfigurationSerializer(serializers.ModelSerializer):
    product_item = ProductItemSerializer()
    variation_option = VariationOptionSerializer()

    class Meta:
        model = ProductConfiguration
        fields = '__all__'


class PromotionCategorySerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    # or use PromotionSerializer() if you need nested data
    promotion = serializers.StringRelatedField()

    class Meta:
        model = PromotionCategory
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    categories = PromotionCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    product_item = ProductItemSerializer()
    # or use ShopOrderSerializer() if you need nested data
    order = serializers.StringRelatedField()

    class Meta:
        model = OrderLine
        fields = '__all__'


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    product_item = ProductItemSerializer()

    class Meta:
        model = ShoppingCartItem
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class UserPaymentMethodSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payment_type = PaymentTypeSerializer()

    class Meta:
        model = UserPaymentMethod
        fields = '__all__'


class UserReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_product = OrderLineSerializer()

    class Meta:
        model = UserReview
        fields = '__all__'


class ShopOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payment_method = UserPaymentMethodSerializer()
    # or use ShippingMethodSerializer() if you need nested data
    shipping_method = serializers.StringRelatedField()

    class Meta:
        model = ShopOrder
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order = OrderLineSerializer()

    class Meta:
        model = OrderHistory
        fields = '__all__'


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Favourite
        fields = '__all__'


class DraftSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    product = ProductSerializer()

    class Meta:
        model = Draft
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    product = ProductSerializer()

    class Meta:
        model = Publish
        fields = '__all__'
