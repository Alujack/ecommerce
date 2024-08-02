from rest_framework import serializers
from base.models import Product, ProductCategory, ProductImage, ProductItem, Stock, Variations, VariationOption, UserReview,Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__' 

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'image']

class VariationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variations
        fields = ['id', 'value']


class VariationOptionSerializer(serializers.ModelSerializer):
    variation = VariationsSerializer(many=True)
    class Meta:
        model = VariationOption
        fields = ['id', 'value']


class ProductItemSerializer(serializers.ModelSerializer):
    variation_options = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductItem
        fields = ['id', 'variation_options']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'quantity', 'store']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'angle']


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ['id', 'review_text', 'rating']


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductItemSerializer(many=True, read_only=True)
    stock = StockSerializer(many=True, read_only=True)
    reviews = UserReviewSerializer(many=True, read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price',
                  'categories', 'images', 'variations', 'stock', 'reviews','store']
