from rest_framework import serializers
from base.models import *


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
        provider_card = data.get('provider_card')
        provider_bank = data.get('provider_bank')

        if provider_card and provider_bank:
            raise serializers.ValidationError(
                "A payment method cannot be linked to both a credit card and bank information."
            )
        if not provider_card and not provider_bank:
            raise serializers.ValidationError(
                "A payment method must be linked to either a credit card or bank information."
            )
        return data

    def create(self, validated_data):
        provider_card_data = validated_data.pop('provider_card', None)
        provider_bank_data = validated_data.pop('provider_bank', None)

        if provider_card_data:
            provider_card = CreditCard.objects.create(**provider_card_data)
            validated_data['provider_card'] = provider_card

        if provider_bank_data:
            provider_bank = BankInformation.objects.create(
                **provider_bank_data)
            validated_data['provider_bank'] = provider_bank

        payment_method = PaymentMethod.objects.create(**validated_data)
        return payment_method


class CheckoutSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField()
    shipping_address = serializers.CharField(max_length=255)
    shipping_method_id = serializers.UUIDField()
    payment_method = serializers.DictField()
    order_total = serializers.IntegerField()
    products = serializers.ListField(
        child=serializers.DictField()
    )

    def create_payment_method(self, validated_data):
        payment_data = validated_data['payment_method']
        provider_card_data = payment_data.get('provider_card')
        provider_bank_data = payment_data.get('provider_bank')

        if provider_card_data:
            credit_card = CreditCard.objects.create(**provider_card_data)
            return PaymentMethod.objects.create(
                customer_id=validated_data['customer_id'],
                provider_card=credit_card
            )
        elif provider_bank_data:
            bank_info = BankInformation.objects.create(**provider_bank_data)
            return PaymentMethod.objects.create(
                customer_id=validated_data['customer_id'],
                provider_bank=bank_info
            )
        else:
            raise serializers.ValidationError("Payment method is required")

    def create(self, validated_data):
        customer_id = validated_data['customer_id']
        shipping_method_id = validated_data['shipping_method_id']
        shipping_address = validated_data['shipping_address']
        order_total = validated_data['order_total']
        products_data = validated_data['products']

        payment_method = self.create_payment_method(validated_data)

        shop_order = ShopOrder.objects.create(
            customer_id=customer_id,
            shipping_address=shipping_address,
            shipping_method_id=shipping_method_id,
            payment_method=payment_method,
            order_total=order_total,
            status='pending'
        )

        for product_data in products_data:
            product = Product.objects.get(id=product_data['product_id'])
            OrderLine.objects.create(
                order=shop_order,
                product=product,
                quantity=product_data['quantity'],
                price=product_data['price']
            )

        return shop_order
