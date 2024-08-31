from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import OrderLine, Category, Product
from .serializers import ProductSerializer
from django.utils.timezone import now, timedelta

User = get_user_model()


def get_order_qty(product):
    """Returns the quantity of orders for a given product in the last month."""
    one_month_ago = now() - timedelta(minutes=30)
    return OrderLine.objects.filter(product=product, created_at__gte=one_month_ago).count()


def get_score(total_orders_in_category, product_order_qty):
    """Calculates the score for a product as a percentage of total orders in the category."""
    if total_orders_in_category == 0:  # Avoid division by zero
        return 0
    return (product_order_qty / total_orders_in_category) * 100


@api_view(['GET'])
def get_bestseller_in_cat(request):
    categories = Category.objects.prefetch_related(
        'products').filter(products__isnull=False).distinct()

    best_sellers = []

    for cat in categories:
        products = Product.objects.filter(categories=cat)
        if not products.exists():
            best_sellers.append({
                'category': cat.category_name,
                'top_products': None
            })
            continue

        order_qty_list = [(product, get_order_qty(product))
                          for product in products]

        # Calculate total orders in this category
        total_orders_in_category = sum(
            order_qty for _, order_qty in order_qty_list)

        # Calculate score for each product and filter out those with a score of 0
        scored_products = [
            (product, get_score(total_orders_in_category, order_qty))
            for product, order_qty in order_qty_list
        ]
        scored_products = [p for p in scored_products if p[1] > 0]

        # Sort products by their score in descending order
        scored_products.sort(key=lambda x: x[1], reverse=True)

        # Get the top 10 products or less if there are fewer than 10
        top_products = scored_products[:10]

        # Serialize the top products
        top_products_serialized = ProductSerializer(
            [product for product, _ in top_products], many=True).data

        best_sellers.append({
            'category': cat.category_name,
            'top_products': top_products_serialized if top_products_serialized else None
        })

    return Response(best_sellers, status=status.HTTP_200_OK)
