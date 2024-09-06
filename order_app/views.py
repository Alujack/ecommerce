from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from base.models import *
from .serializers import *


@api_view(['GET'])
def get_order_history(request, pk):
    try:
        user = User.objects.get(id=pk)
        # Get all orders for the user
        orders = ShopOrder.objects.filter(customer=user)

        # Create response data list
        response_data = []

        # Iterate over each order and build the response structure
        for order in orders:
            # Get all order lines for the current order
            order_lines = OrderLine.objects.filter(order=order)

            # Collect product data for each order line
            products = []
            for line in order_lines:
                product = line.product
                product_data = ProductSerializer(product).data
                products.append(product_data)  # Append each product's data

            # Add order and its associated products to response data
            response_data.append({
                "id": order.id,
                "created_at": order.created_at,
                "user": str(user.id),
                "order": order.id,
                "products": products  # This remains a list, with individual product data
            })

        return Response(response_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
