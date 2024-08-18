
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from base.models import *
from .serializers import *
User = get_user_model()


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VariationsViewSet(viewsets.ModelViewSet):
    queryset = Variations.objects.all()
    serializer_class = VariationsSerializer


class VariationOptionViewSet(viewsets.ModelViewSet):
    queryset = VariationOption.objects.all()
    serializer_class = VariationOptionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer



class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
