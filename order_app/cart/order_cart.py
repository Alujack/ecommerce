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

        if not product_id or not qty:
            return Response({"error": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)

        # Update or create the cart item based on customer and product
        cart_item, created = ShoppingCartItem.objects.update_or_create(
            customer=user,
            product=product,
            defaults={'qty': qty}
        )

        if not created:
            # If the item already existed, just update the quantity
            cart_item.qty = int(qty)
            cart_item.save()

        return Response(status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_favourite_items(request, pk):
    try:
        user = User.objects.get(id=pk)
        # Use query_params to get the productId from the URL
        product_id = request.query_params.get('productId')
        if product_id is None:
            return Response({'detail': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)
        favourite = Favourite.objects.update_or_create(
            user=user,
            product=product,
        )
        return Response(status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_favourite_items(request):
    try:
        user = request.query_params.get('user')
        favourites = Favourite.objects.filter(user=user)
        product_list = []
        for fav in favourites:
            product = Product.objects.get(id=fav.product.id)
            product_list.append(product)
        serializers = ProductSerializer(product_list, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete_favourite(request):
    try:
        user = request.query_params.get('user')
        product_id = request.query_params.get('productId')
        fav = Favourite.objects.get(user=user, product=product_id)
        if fav:
            fav.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete_cart(request):
    try:
        user = request.query_params.get('user')
        product_id = request.query_params.get('productId')
        cart = ShoppingCartItem.objects.get(customer=user, product=product_id)
        if cart:
            cart.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete_all_cart(request):
    try:
        user = request.query_params.get('user')
        cart = ShoppingCartItem.objects.filter(customer=user)
        if cart:
            cart.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)