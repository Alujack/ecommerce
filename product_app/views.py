from rest_framework import generics
from .serializers import ProductSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from base.models import ProductCategory, Variations, VariationOption, Product, ProductImage, ProductItem, Stock
from .serializers import *
User = get_user_model()


# Store Views


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


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


class ProductItemViewSet(viewsets.ModelViewSet):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
