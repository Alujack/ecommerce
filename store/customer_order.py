from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *
from base.models import *
User = get_user_model()


@api_view(['GET'])
def get_order_line(request):
    store_id = request.query_params.get('store')
    store = Store.objects.get(id=store_id)
    # print(store.id)
    order_list = customerOrder.objects.filter(store_id=store.id)
    order_line = []
    for item in order_list:
        shop_order = ShopOrder.objects.get(id=item.order.id)
        shop_order_data = ShopOrderSerializer(shop_order).data
        print(shop_order.customer)
        user = User.objects.get(id=shop_order.customer_id)
        user_data = UserSerializer(user).data
        order_line.append({
            'order': shop_order_data,
            'customer': user_data
        })
    print(order_line)
    data = {
        'order_line': order_line
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_store_orders(request):
    store_id = request.query_params.get('store')

    # Fetch the store and associated products
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get all products in the store
    products_in_store = Product.objects.filter(store=store)

    # Get all order lines that are associated with the store's products
    order_lines = OrderLine.objects.filter(product__in=products_in_store)

    # Aggregate the data for each order and the associated customer
    orders_data = []
    for order_line in order_lines:
        shop_order = order_line.order  # Get the ShopOrder for the order line
        customer = shop_order.customer

        # Prepare order data
        orders_data.append({
            'product_id': order_line.product.product_id,
            'store_name': store.name,
            'customer_email': customer.email if customer else 'Guest',
            'order_total': shop_order.order_total,
            'quantity': order_line.quantity,
            'status': shop_order.status,
            'order_date': shop_order.order_date
        })

    # Return the aggregated data
    return Response(orders_data, status=status.HTTP_200_OK)

