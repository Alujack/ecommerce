from rest_framework import serializers
from base.models import Store, ProductCategory, Variations, VariationOption, Product, ProductImage, ProductItem, Stock, Publish, Draft


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class VariationsSerializer(serializers.ModelSerializer):
    variation_option = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Variations
        fields = ['id', 'attribute_type', 'variation_option']


class ProductItemSerializer(serializers.ModelSerializer):
    variation_options = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product_name'] = instance.product.name
        return representation


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    product_item = ProductItemSerializer(
        source='product_item_variation', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    categories = ProductCategorySerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)
    variations = VariationsSerializer(many=True, read_only=True)

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
