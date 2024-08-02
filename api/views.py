# from rest_framework import viewsets
# from base.models import (
#     User, Stock, Store, CustomerList, Address, ProductCategory, Product, ProductItem, Variations,
#     VariationOption, Promotion, PromotionCategory, OrderLine, ShoppingCartItem,
#     PaymentType, UserPaymentMethod, UserReview, ShopOrder, OrderHistory, ShippingMethod, Favourite, Draft, Publish
# )
# from .serializers import (
#     UserSerializer, StockSerializer, StoreSerializer, CustomerListSerializer, AddressSerializer,
#     ProductCategorySerializer, ProductSerializer, ProductItemSerializer, VariationSerializer,
#     VariationOptionSerializer, ProductConfigurationSerializer, PromotionSerializer,
#     PromotionCategorySerializer, OrderLineSerializer, ShoppingCartItemSerializer,
#     PaymentTypeSerializer, UserPaymentMethodSerializer, UserReviewSerializer, ShopOrderSerializer,
#     OrderHistorySerializer, ShippingMethodSerializer, FavouriteSerializer, DraftSerializer, PublishSerializer
# )
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from base.models import User
# from django.http import HttpResponse


# @csrf_exempt
# def create(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         users = User.objects.create(
#             email=email, password_hash=password)
#         users.save()
#         return HttpResponse('success')
#     return HttpResponse('fail')

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class StockViewSet(viewsets.ModelViewSet):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer


# class StoreViewSet(viewsets.ModelViewSet):
#     queryset = Store.objects.all()
#     serializer_class = StoreSerializer


# class CustomerListViewSet(viewsets.ModelViewSet):
#     queryset = CustomerList.objects.all()
#     serializer_class = CustomerListSerializer


# class AddressViewSet(viewsets.ModelViewSet):
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer


# class ProductCategoryViewSet(viewsets.ModelViewSet):
#     queryset = ProductCategory.objects.all()
#     serializer_class = ProductCategorySerializer


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductItemViewSet(viewsets.ModelViewSet):
#     queryset = ProductItem.objects.all()
#     serializer_class = ProductItemSerializer


# class VariationViewSet(viewsets.ModelViewSet):
#     queryset = Variations.objects.all()
#     serializer_class = VariationSerializer


# class VariationOptionViewSet(viewsets.ModelViewSet):
#     queryset = VariationOption.objects.all()
#     serializer_class = VariationOptionSerializer


# class ProductConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = ProductConfiguration.objects.all()
#     serializer_class = ProductConfigurationSerializer


# class PromotionViewSet(viewsets.ModelViewSet):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer


# class PromotionCategoryViewSet(viewsets.ModelViewSet):
#     queryset = PromotionCategory.objects.all()
#     serializer_class = PromotionCategorySerializer


# class OrderLineViewSet(viewsets.ModelViewSet):
#     queryset = OrderLine.objects.all()
#     serializer_class = OrderLineSerializer


# class ShoppingCartItemViewSet(viewsets.ModelViewSet):
#     queryset = ShoppingCartItem.objects.all()
#     serializer_class = ShoppingCartItemSerializer


# class PaymentTypeViewSet(viewsets.ModelViewSet):
#     queryset = PaymentType.objects.all()
#     serializer_class = PaymentTypeSerializer


# class UserPaymentMethodViewSet(viewsets.ModelViewSet):
#     queryset = UserPaymentMethod.objects.all()
#     serializer_class = UserPaymentMethodSerializer


# class UserReviewViewSet(viewsets.ModelViewSet):
#     queryset = UserReview.objects.all()
#     serializer_class = UserReviewSerializer


# class ShopOrderViewSet(viewsets.ModelViewSet):
#     queryset = ShopOrder.objects.all()
#     serializer_class = ShopOrderSerializer


# class OrderHistoryViewSet(viewsets.ModelViewSet):
#     queryset = OrderHistory.objects.all()
#     serializer_class = OrderHistorySerializer


# class ShippingMethodViewSet(viewsets.ModelViewSet):
#     queryset = ShippingMethod.objects.all()
#     serializer_class = ShippingMethodSerializer


# class FavouriteViewSet(viewsets.ModelViewSet):
#     queryset = Favourite.objects.all()
#     serializer_class = FavouriteSerializer


# class DraftViewSet(viewsets.ModelViewSet):
#     queryset = Draft.objects.all()
#     serializer_class = DraftSerializer


# class PublishViewSet(viewsets.ModelViewSet):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializer
