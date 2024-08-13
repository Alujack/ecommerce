
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, ProductCategory, Variations, VariationOption, ProductItem, Stock, ProductImage, Publish, Draft
from .serializers import ProductSerializer, ProductCategorySerializer, VariationsSerializer, VariationOptionSerializer, ProductItemSerializer, StockSerializer, ProductImageSerializer
from django.shortcuts import get_object_or_404
