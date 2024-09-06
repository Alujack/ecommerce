from rest_framework import generics
from .filters import ProductFilter
from .serializers import ProductSerializer
from base.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', None)
    products_starting_with_name = Product.objects.none()
    products_containing_query = Product.objects.none()

    if query:
        # Step 1: Products where name starts with the query
        products_starting_with_name = Product.objects.filter(
            name__istartswith=query)

        # Step 2: Products where name, short_description, or description contains the query
        products_containing_query = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).exclude(id__in=products_starting_with_name.values('id'))

    # Combine both querysets
    products = products_starting_with_name | products_containing_query

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_relate(request, pk):
    cat = Product.objects.get(id=pk).categories.first()
    products = Product.objects.filter(categories=cat)
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_filter_products(request):
    # Get the min and max price from query parameters
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)

    # Filter products based on price range
    products = Product.objects.all()

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    # Serialize the products and return the response
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
