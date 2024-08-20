from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customer-lists', CustomerListViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'product-categories', CategoryViewSet)
router.register(r'variations', VariationsViewSet)
router.register(r'variation-options', VariationOptionViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'stock', StockViewSet)
router.register(r'user-reviews', UserReviewViewSet)
router.register(r'drafts', DraftViewSet)
router.register(r'publish', PublishViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'promotion-categories', PromotionCategoryViewSet)
router.register(r'shopping-cart-items', ShoppingCartItemViewSet)
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'user-payment-methods', UserPaymentMethodViewSet)
router.register(r'shop-orders', ShopOrderViewSet)
router.register(r'order-lines', OrderLineViewSet)
router.register(r'order-histories', OrderHistoryViewSet)
router.register(r'shipping-methods', ShippingMethodViewSet)
router.register(r'favourites', FavouriteViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('auth_app.urls')),
    path('store/', include('store.urls')),
    path('product/', include('product_app.urls')),
    path('admin_manage/', include('admin_app.urls')),
    path('inventory/', include('inventory.urls')),
    path('shipping_app/', include('shipping_app.urls'))

]
