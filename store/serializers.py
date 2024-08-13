from base.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerList
        fields = '__all__'
        
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields='__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields ='__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class ProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItem
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