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
    one_month_ago = now() - timedelta(days=30)
    return OrderLine.objects.filter(product=product, created_at__gte=one_month_ago).count()


def get_score(total_orders_in_category, product_order_qty):
    """Calculates the score for a product as a percentage of total orders in the category."""
    if total_orders_in_category == 0:  # Avoid division by zero
        return 0
    return (product_order_qty / total_orders_in_category) * 100


@api_view(['GET'])
def get_bestseller_in_cat(request):
    category_id = request.query_params.get('category_id')
    if category_id:
        # Get best sellers for a specific category
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(categories=category)
        if not products.exists():
            return Response({
                'category': category.category_name,
                'top_products': None
            }, status=status.HTTP_200_OK)

        order_qty_list = [(product, get_order_qty(product))
                          for product in products]

        total_orders_in_category = sum(
            order_qty for _, order_qty in order_qty_list)

        scored_products = [
            (product, get_score(total_orders_in_category, order_qty))
            for product, order_qty in order_qty_list
        ]
        scored_products = [p for p in scored_products if p[1] > 0]

        scored_products.sort(key=lambda x: x[1], reverse=True)

        top_products = scored_products[:10]

        top_products_serialized = ProductSerializer(
            [product for product, _ in top_products], many=True).data

        return Response({
            'category': category.category_name,
            'top_products': top_products_serialized if top_products_serialized else None
        }, status=status.HTTP_200_OK)

    else:
        # Get best sellers for all categories
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

            total_orders_in_category = sum(
                order_qty for _, order_qty in order_qty_list)

            scored_products = [
                (product, get_score(total_orders_in_category, order_qty))
                for product, order_qty in order_qty_list
            ]
            scored_products = [p for p in scored_products if p[1] > 0]

            scored_products.sort(key=lambda x: x[1], reverse=True)

            top_products = scored_products[:10]

            top_products_serialized = ProductSerializer(
                [product for product, _ in top_products], many=True).data

            best_sellers.append({
                'category': cat.category_name,
                'top_products': top_products_serialized if top_products_serialized else None
            })

        return Response(best_sellers, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bestsellers(request):
    # Fetch all products
    products = Product.objects.all()

    # If there are no products, return an empty response
    if not products.exists():
        return Response({"detail": "No products found."}, status=status.HTTP_200_OK)

    # List to hold (product, order_qty) tuples
    order_qty_list = [(product, get_order_qty(product))
                      for product in products]

    # Sum the total number of orders across all products
    total_orders = sum(order_qty for _, order_qty in order_qty_list)

    # Calculate scores for each product based on the total orders
    scored_products = [
        (product, get_score(total_orders, order_qty))
        for product, order_qty in order_qty_list
    ]

    # Filter out products with a score of 0
    scored_products = [p for p in scored_products if p[1] > 0]

    # Sort products by their score in descending order
    scored_products.sort(key=lambda x: x[1], reverse=True)

    # Limit to the top 10 best-selling products (or any number you prefer)
    top_products = scored_products[:10]

    # Serialize the top products
    top_products_serialized = ProductSerializer(
        [product for product, _ in top_products], many=True).data

    # Return the top products
    return Response(top_products_serialized if top_products_serialized else None, status=status.HTTP_200_OK)
