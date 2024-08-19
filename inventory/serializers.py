from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'
