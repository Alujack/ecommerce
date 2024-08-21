from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from order_app.serializers import *
from base.models import *


@api_view(['GET'])
def get_cart_items(request, pk):
    try:
        user = User.objects.get(id=pk)
        cart_items = ShoppingCartItem.objects.filter(customer=user)
        cart_item_list = []
        for cart in cart_items:
            product = Product.objects.get(id=cart.product.id)
            cart_serializer = ShoppingCartItemSerializer(cart).data
            product_serializer = ProductSerializer(product).data
            cart_item_list.append(
                {'cart_item': cart_serializer, 'products': product_serializer})
        return Response(cart_item_list, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
