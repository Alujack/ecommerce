from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import Category
from .serializers import *
from django.db.models import Sum
User = get_user_model()


@api_view(['GET'])
def get_product_by_category(request, pk=None):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(categories=category)
    product_serializers = ProductSerializer(products, many=True)

    return Response(product_serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_products_by_store(request, pk=None):
    try:
        store = Store.objects.get(id=pk)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

    # Fetch products for the store
    products = Product.objects.filter(store=store)

    if not products.exists():
        return Response({"error": "No products found for this store"}, status=status.HTTP_404_NOT_FOUND)

    # Create a list to store the product data
    products_data = []

    for product in products:
        # Aggregate total stock quantity for each product
        total_stock_quantity = Stock.objects.filter(product=product).aggregate(
            total_quantity=Sum('quantity'))['total_quantity'] or 0

        # Append product data with total stock quantity
        products_data.append({
            "id": product.id,
            "product_id": product.product_id,
            "name": product.name,
            "short_description": product.short_description,
            "description": product.description,
            "price": product.price,
            "image": product.image.url if product.image else None,
            "total_stock_quantity": total_stock_quantity
        })

    return Response(products_data, status=status.HTTP_200_OK)


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


@api_view(['GET'])
def get_product_detail(request, pk=None):
    try:
        product = Product.objects.get(id=pk)
    except product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    product_serializer = ProductSerializer(product)
