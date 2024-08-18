from rest_framework import serializers
from base.models import Store, Category, Variations, VariationOption, Product, ProductImage, Stock, Publish, Draft


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    stock = StockSerializer(many=True,read_only=True)
    variations = VariationsSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = '__all__'


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'
