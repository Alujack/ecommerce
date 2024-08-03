from rest_framework import serializers
from base.models import Product, ProductCategory, ProductImage, Variations, VariationOption, Stock, Store, UserReview


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'angle']


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id', 'value']


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = ['id', 'attribute_type']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'quantity', 'variation', 'store']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ['id', 'review_text', 'rating']


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer()
    variations = VariationSerializer()
    stock = StockSerializer()
    reviews = UserReviewSerializer()
    store = StoreSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories',
                  'variations', 'stock', 'reviews', 'store']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        variations_data = validated_data.pop('variations')
        stock_data = validated_data.pop('stock')
        reviews_data = validated_data.pop('reviews')
        store_data = validated_data.pop('store')

        store, created = Store.objects.get_or_create(**store_data)

        product = Product.objects.create(store=store, **validated_data)

        for category_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                **category_data)
            product.categories.add(category)

        for variation_data in variations_data:
            variation_options_data = variation_data.pop('variation_options')
            variation = Variations.objects.create(
                product=product, **variation_data)
            for option_data in variation_options_data:
                option, created = VariationOption.objects.get_or_create(
                    **option_data)
                variation.variation_options.add(option)

        for stock_item in stock_data:
            Stock.objects.create(product=product, **stock_item)

        for review_data in reviews_data:
            UserReview.objects.create(product=product, **review_data)

        return product
