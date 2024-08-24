
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import *
from .serializers import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
User = get_user_model()


@api_view(['GET'])
def get_parents_categories(request):
    try:
        parent_categories = Category.objects.all()
        serializers = CategorySerializer(parent_categories, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_sub_categories(request):
    parent = request.query_params.get('parent')
    try:
        sub_categories = Category.objects.filter(parent_category=parent)
        serializers = CategorySerializer(data=sub_categories, many=True)
        if serializers.is_valid():
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_404_NOT_FOUND)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_product_by_category(request):
    id = request.query_params.get('category')
    try:
        category = Category.objects.get(id=id)
        products = Product.objects.filter(categories=category)
        serializers = ProductSerializer(data=products, many=True)
        if serializers.is_valid():
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_404_NOT_FOUND)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_new_arrival_products(request):
    hours_ago = timezone.now() - timedelta(minutes=2)
    print(hours_ago)
    try:
        # Filter products created within the last 2 hours
        products = Product.objects.filter(created_at__gte=hours_ago)

        # Serialize the products
        serializer = ProductSerializer(products, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_new_arrival_products_in_category(request):
    category = request.query_params.get('category')
    hours_ago = timezone.now() - timedelta(minutes=60)
    print(hours_ago)
    try:
        # Filter products created within the last 2 hours
        products = Product.objects.filter(
            created_at__gte=hours_ago, categories=category)

        # Serialize the products
        serializer = ProductSerializer(products, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# myself
 
# @api_view(['GET'])
# def get_cat_contain_product(request):
#     # Get all categories
#     categories = Category.objects.all()

#     # Filter categories that contain products
#     category_list = []
#     for category in categories:
#         if Product.objects.filter(categories=category).exists():
#             category_list.append(category)

#     # Serialize the category list
#     serializer = CategorySerializer(category_list, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)


#this is ai

# @api_view(['GET'])
# def get_cat_contain_product(request):
#     # Select related products along with categories
#     categories = Category.objects.filter(
#         product__isnull=False).select_related('products').distinct()

#     # Serialize the category list
#     serializer = CategorySerializer(categories, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)

# this ai 

# @api_view(['GET'])
# def get_cat_contain_product(request):
#     # Annotate categories with the count of related products
#     categories = Category.objects.annotate(
#         product_count=Count('products')).filter(product_count__gt=0)

#     # Serialize the category list
#     serializer = CategorySerializer(categories, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)

# this is me

@api_view(['GET'])
def get_cat_contain_product(request):
    categories = Category.objects.prefetch_related(
        'products').filter(products__isnull=False).distinct()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
