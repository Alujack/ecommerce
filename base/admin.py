from django.contrib import admin
from .models import (
    User, CustomerList, Address, Store, ProductCategory, Variations,
    VariationOption, Product, ProductImage, ProductItem, Stock,
    UserReview, Draft, Publish, Promotion, PromotionCategory,
    OrderLine, ShoppingCartItem, PaymentType, UserPaymentMethod,
    ShopOrder, OrderHistory, ShippingMethod, Favourite
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'role')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id', 'price', 'store')
    search_fields = ('name', 'product_id', 'description')
    list_filter = ('store', 'categories')


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_option')
    search_fields = ('product__name', 'variation_option__value')
    list_filter = ('product',)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product_item_variation', 'quantity', 'store')
    search_fields = ('product_item_variation__product__name', 'store__name')
    list_filter = ('store',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'angle')
    search_fields = ('product__name', 'angle')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller')
    search_fields = ('name', 'seller__email')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'store')
    search_fields = ('category_name', 'store__name')


@admin.register(Variations)
class VariationsAdmin(admin.ModelAdmin):
    list_display = ('attribute_type', 'category')
    search_fields = ('attribute_type', 'category__category_name')


@admin.register(VariationOption)
class VariationOptionAdmin(admin.ModelAdmin):
    list_display = ('variation', 'value')
    search_fields = ('variation__attribute_type', 'value')


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating')
    search_fields = ('user__email', 'product__name', 'rating')


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('store', 'product')
    search_fields = ('store__name', 'product__name')


@admin.register(Publish)
class PublishAdmin(admin.ModelAdmin):
    list_display = ('store', 'product')
    search_fields = ('store__name', 'product__name')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'end_date')


@admin.register(PromotionCategory)
class PromotionCategoryAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'category')
    search_fields = ('promotion__name', 'category__category_name')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'order', 'quantity', 'price')
    search_fields = ('product_item__product__name', 'order__id')
    list_filter = ('order',)


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_item', 'qty')
    search_fields = ('customer__email', 'product_item__product__name')


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('type_value',)
    search_fields = ('type_value',)


@admin.register(UserPaymentMethod)
class UserPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_type', 'provider')
    search_fields = ('user__email', 'provider')


@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'payment_method',
                    'shipping_address', 'order_total', 'status')
    search_fields = ('user__email', 'shipping_address')
    list_filter = ('status', 'order_date')


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order')
    search_fields = ('user__email', 'order__id')


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'price')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__email', 'product__name')


@admin.register(CustomerList)
class CustomerListAdmin(admin.ModelAdmin):
    list_display = ('store', 'user')
    search_fields = ('store__name', 'user__email')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country')
    search_fields = ('user__email', 'city', 'country')
