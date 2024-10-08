from rest_framework import viewsets
from base.models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerListViewSet(viewsets.ModelViewSet):
    queryset = CustomerList.objects.all()
    serializer_class = CustomerListSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer


class VariationsViewSet(viewsets.ModelViewSet):
    queryset = Variations.objects.all()
    serializer_class = VariationsSerializer


class VariationOptionViewSet(viewsets.ModelViewSet):
    queryset = VariationOption.objects.all()
    serializer_class = VariationOptionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class UserReviewViewSet(viewsets.ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = UserReviewSerializer


class DraftViewSet(viewsets.ModelViewSet):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer


class PublishViewSet(viewsets.ModelViewSet):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class PromotionCategoryViewSet(viewsets.ModelViewSet):
    queryset = PromotionCategory.objects.all()
    serializer_class = PromotionCategorySerializer


class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCartItem.objects.all()
    serializer_class = ShoppingCartItemSerializer


class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class UserPaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = UserPaymentMethodSerializer


class ShopOrderViewSet(viewsets.ModelViewSet):
    queryset = ShopOrder.objects.all()
    serializer_class = ShopOrderSerializer


class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer


class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer


class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
