from rest_framework import serializers
from base.models import Category


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
