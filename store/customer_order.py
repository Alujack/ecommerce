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
