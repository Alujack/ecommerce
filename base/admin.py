from django.contrib import admin
from .models import (
    User, Stock, Store, CustomerList, Address, ProductCategory,
    Product, ProductItem, Variation,
    VariationOption, ProductConfiguration, Promotion, PromotionCategory,
    OrderLine, ShoppingCartItem, PaymentType, UserPaymentMethod,
    UserReview, ShopOrder, OrderHistory, ShippingMethod, Favourite, Draft, Publish
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('seller',  'name', 'created_at')


@admin.register(CustomerList)
class CustomerListAdmin(admin.ModelAdmin):
    list_display = ('store', 'user')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'street_number', 'address_line1',
                    'address_line2', 'city', 'state', 'postal_code', 'country')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent_category', 'image')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name',
                    'description', 'product_image', 'price')


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_in_stock')


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute_type')


@admin.register(VariationOption)
class VariationOptionAdmin(admin.ModelAdmin):
    list_display = ('variation', 'option_value')


@admin.register(ProductConfiguration)
class ProductConfigurationAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'variation_option')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',
                    'discount_percentage', 'start_date', 'end_date')


@admin.register(PromotionCategory)
class PromotionCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'promotion')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'order', 'quantity', 'price')


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_item', 'qty')


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('type_value',)


@admin.register(UserPaymentMethod)
class UserPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_type', 'provider',
                    'card_number', 'expiry_date')


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_product', 'review_text', 'rating')


@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'payment_method',
                    'shipping_address', 'shipping_method', 'order_total', 'status')


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order')


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


@admin.register(Draft)
class draftAdmin(admin.ModelAdmin):
    list_display = ('store', 'product')


@admin.register(Publish)
class PublishAdmin(admin.ModelAdmin):
    list_display = ('store', 'product')
