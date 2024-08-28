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


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'


class BankInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInformation
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    provider_card = CreditCardSerializer(required=False)
    provider_bank = BankInformationSerializer(required=False)

    class Meta:
        model = PaymentMethod
        fields = '__all__'

    def validate(self, data):
        if data.get('provider_card') and data.get('provider_bank'):
            raise serializers.ValidationError(
                "A payment method cannot be linked to both a credit card and bank information.")
        if not data.get('provider_card') and not data.get('provider_bank'):
            raise serializers.ValidationError(
                "A payment method must be linked to either a credit card or bank information.")
        return data

    def create(self, validated_data):
        card_data = validated_data.pop('provider_card', None)
        bank_data = validated_data.pop('provider_bank', None)

        if card_data:
            card = CreditCard.objects.create(**card_data)
            validated_data['provider_card'] = card
        elif bank_data:
            bank = BankInformation.objects.create(**bank_data)
            validated_data['provider_bank'] = bank

        return PaymentMethod.objects.create(**validated_data)


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = '__all__'


class ShopOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOrder
        fields = '__all__'
