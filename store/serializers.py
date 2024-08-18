from base.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

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
    
class AddressSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True)
    class Meta:
        model = Address
        fields = '__all__'

class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerList
        fields = '__all__'
        

class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Store
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_id = address_data.get('id')
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            address = Address.objects.create(**address_data)
        store = Store.objects.create(address=address, **validated_data)
        return store

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address_id = address_data.get('id')
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            address = Address.objects.create(**address_data)
        instance.address = address
        instance.name = validated_data.get('name', instance.name)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.save()
        return instance
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
class CustomerListSerailizers(serializers.ModelSerializer):
    class Mata:
        models= CustomerList
        fields = '__all__'