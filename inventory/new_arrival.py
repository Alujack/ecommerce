from django.db.models import Prefetch, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Category, Product
from .serializers import ProductSerializer
from django.utils.timezone import now, timedelta


@api_view(['GET'])
def get_new_in_cat(request):
    # Calculate the date for one month ago
    one_month_ago = now() - timedelta(days=30)

    # Get the category_id from request parameters, if provided
    category_id = request.query_params.get('category_id')

    if category_id:
        # Filter categories based on category_id if provided
        categories = Category.objects.prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(
                    created_at__gte=one_month_ago).order_by(
                    '-created_at'),
                to_attr='new_arrivals'
            )
        ).filter(pk=category_id, products__created_at__gte=one_month_ago).distinct()

        if not categories.exists():
            return Response({"detail": "Category not found or has no new arrivals."}, status=status.HTTP_404_NOT_FOUND)

        # Get the first category (since there should only be one based on category_id)
        category = categories.first()

        # Prepare the response data for the specific category
        response_data = {
            'category': category.category_name,
            'new_arrivals': ProductSerializer(category.new_arrivals, many=True).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        # Retrieve all categories with products created in the last month
        categories = Category.objects.prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(created_at__gte=one_month_ago).order_by(
                    '-created_at'),
                to_attr='new_arrivals'
            )
        ).filter(products__created_at__gte=one_month_ago).distinct()

        # Prepare the response data for all categories
        response_data = [
            {
                'category': category.category_name,
                'new_arrivals': ProductSerializer(category.new_arrivals, many=True).data
            }
            for category in categories
        ]

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_new_arrivals(request):
    # Calculate the date for one month ago
    one_month_ago = now() - timedelta(days=30)

    # Fetch all categories with products that were created in the last month, ordered by newest first
    categories = Category.objects.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(created_at__gte=one_month_ago).order_by(
                '-created_at'),  # Order by newest first
            to_attr='new_arrivals'
        )
    ).filter(products__created_at__gte=one_month_ago).distinct()

    # Prepare the response data: a flat list of products across all categories
    response_data = []
    for category in categories:
        serialized_products = ProductSerializer(
            category.new_arrivals, many=True).data
        # Add the products to the flat list
        response_data.extend(serialized_products)

    return Response(response_data, status=status.HTTP_200_OK)
