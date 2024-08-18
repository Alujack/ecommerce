from django.contrib import admin
from .models import (
    User, CustomerList, Address, Store, Category, Variations, VariationOption, Product,
    ProductImage, Stock, TechnicalDetail, ProductRecommendation, Pricing, CustomerReview,
    Draft, Publish, Promotion, PromotionCategory, ShoppingCartItem, PaymentType,
    PaymentMethod, ShopOrder, OrderLine, OrderHistory, ShippingMethod, Favourite, Question,
    Answer
)

# Register your models here.
admin.site.register(User)
admin.site.register(CustomerList)
admin.site.register(Address)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Variations)
admin.site.register(VariationOption)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Stock)
admin.site.register(TechnicalDetail)
admin.site.register(ProductRecommendation)
admin.site.register(Pricing)
admin.site.register(CustomerReview)
admin.site.register(Draft)
admin.site.register(Publish)
admin.site.register(Promotion)
admin.site.register(PromotionCategory)
admin.site.register(ShoppingCartItem)
admin.site.register(PaymentType)
admin.site.register(PaymentMethod)
admin.site.register(ShopOrder)
admin.site.register(OrderLine)
admin.site.register(OrderHistory)
admin.site.register(ShippingMethod)
admin.site.register(Favourite)
admin.site.register(Question)
admin.site.register(Answer)
