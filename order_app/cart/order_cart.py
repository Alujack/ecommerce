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
    

@api_view(['POST'])
def add_cart_items(request, pk):
    try:
        user = User.objects.get(id=pk)
        product_id = request.query_params.get('productId')
        qty = request.query_params.get('qty')
        product = Product.objects.get(id=product_id)
        cart_items = ShoppingCartItem.objects.update_or_create(
            customer=user,
            product=product,
            qty=qty
        )
        return Response( status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_favourite_items(request, pk):
    try:
        user = User.objects.get(id=pk)
        product_id = request.query_params.get('productId')
        product = Product.objects.get(id=product_id)
        favourite = Favourite.objects.update_or_create(
            user=user,
            product=product,
        )
        return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_favourite_items(request, pk):
    try:
        user = User.objects.get(id=pk)
        products = Favourite.objects.filter(user=user)
        serializers = FavouriteSerializer(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
