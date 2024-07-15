from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, StockViewSet, StoreViewSet, CustomerListViewSet, AddressViewSet, ProductCategoryViewSet,
    ProductViewSet, ProductItemViewSet, VariationViewSet, VariationOptionViewSet, ProductConfigurationViewSet,
    PromotionViewSet, PromotionCategoryViewSet, OrderLineViewSet, ShoppingCartItemViewSet, PaymentTypeViewSet,
    UserPaymentMethodViewSet, UserReviewViewSet, ShopOrderViewSet, OrderHistoryViewSet, ShippingMethodViewSet,
    FavouriteViewSet, DraftViewSet, PublishViewSet, create
)
from auth_app.views import *
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'customer-lists', CustomerListViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-items', ProductItemViewSet)
router.register(r'variations', VariationViewSet)
router.register(r'variation-options', VariationOptionViewSet)
router.register(r'product-configurations', ProductConfigurationViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'promotion-categories', PromotionCategoryViewSet)
router.register(r'order-lines', OrderLineViewSet)
router.register(r'shopping-cart-items', ShoppingCartItemViewSet)
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'user-payment-methods', UserPaymentMethodViewSet)
router.register(r'user-reviews', UserReviewViewSet)
router.register(r'shop-orders', ShopOrderViewSet)
router.register(r'order-histories', OrderHistoryViewSet)
router.register(r'shipping-methods', ShippingMethodViewSet)
router.register(r'favourites', FavouriteViewSet)
router.register(r'drafts', DraftViewSet)
router.register(r'publishes', PublishViewSet)
# router.register(r'login', login_view)
# router.register(r'register', register_view)
# router.register(r'social_view', register_social_view)



urlpatterns = [
    path('', include(router.urls)),
    path('auth-app/', include('auth_app.urls')),
    path('store/', include('store.urls')),
]
