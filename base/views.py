from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateSellerView(generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class CreateStoreView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class PostProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['POST'])
def add_to_cart(request):
    user = User.objects.get(id=request.data['user_id'])
    cart, created = ShoppingCart.objects.get_or_create(user=user)
    product_item = ProductItem.objects.get(id=request.data['product_item_id'])
    qty = request.data['qty']

    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart, product_item=product_item)
    if not created:
        cart_item.qty += qty
    else:
        cart_item.qty = qty
    cart_item.save()

    serializer = ShoppingCartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
def checkout_payment(request):
    user = User.objects.get(id=request.data['user_id'])
    cart = ShoppingCart.objects.get(user=user)
    payment_method = UserPaymentMethod.objects.get(
        id=request.data['payment_method_id'])
    shipping_address = request.data['shipping_address']
    shipping_method = ShippingMethod.objects.get(
        id=request.data['shipping_method_id'])
    order_total = sum(item.product_item.product.price *
                      item.qty for item in cart.shoppingcartitem_set.all())
    order_status = OrderStatus.objects.get(status='Pending')

    order = ShopOrder.objects.create(
        user=user,
        payment_method=payment_method,
        shipping_address=shipping_address,
        shipping_method=shipping_method,
        order_total=order_total,
        order_status=order_status
    )

    for item in cart.shoppingcartitem_set.all():
        OrderLine.objects.create(
            product_item=item.product_item,
            order=order,
            quantity=item.qty,
            price=item.product_item.product.price * item.qty
        )

    cart.shoppingcartitem_set.all().delete()

    serializer = ShopOrderSerializer(order)
    return Response(serializer.data)
