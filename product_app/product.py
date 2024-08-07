from rest_framework import generics
from .serializers import ProductSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from base.models import ProductCategory, Variations, VariationOption, Product, ProductImage, ProductItem, Stock
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()


@api_view(['GET'])
def get_product_by_category(request, pk=None):
    try:
        category = ProductCategory.objects.get(id=pk)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(categories=category)
    product_serializers = ProductSerializer(products, many=True)

    return Response(product_serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product_by_store(request, pk=None):
    try:
        store = Store.objects.get(id=pk)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)
    products = Product.objects.filter(store=store)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_product(request):
    print("Received product data:", request.data)  # Debug print

    serializers = ProductSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    else:
        print("Validation errors:", serializers.errors)  # Debug print
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request):
    # Extract the list of product IDs from the request data
    product_ids = request.data.get('productIds')

    # Check if the product_ids is a list
    if not isinstance(product_ids, list):
        return Response({'error': 'Invalid data format. Expected a list of product IDs.'}, status=status.HTTP_400_BAD_REQUEST)

    # Iterate over the product IDs and attempt to delete each product
    for product_id in product_ids:
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
        except Product.DoesNotExist:
            return Response({'error': f'Product with id {product_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Products deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
