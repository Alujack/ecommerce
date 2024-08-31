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

    # Filter categories based on category_id if provided
    if category_id:
        try:
            categories = Category.objects.filter(
                pk=category_id,
                products__created_at__gte=one_month_ago
            ).prefetch_related(
                Prefetch(
                    'products',
                    queryset=Product.objects.filter(
                        created_at__gte=one_month_ago),
                    to_attr='new_arrivals'
                )
            )
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        categories = Category.objects.prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(created_at__gte=one_month_ago),
                to_attr='new_arrivals'
            )
        ).filter(products__created_at__gte=one_month_ago).distinct()

    # Prepare the response data
    response_data = []
    for category in categories:
        serialized_products = ProductSerializer(
            category.new_arrivals, many=True).data
        response_data.append({
            'category': category.category_name,
            'new_arrivals': serialized_products
        })

    return Response(response_data, status=status.HTTP_200_OK)
