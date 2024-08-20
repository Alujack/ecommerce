from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'credit-cards', CreditCardViewSet)
router.register(r'bank-information', BankInformationViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'checkout', CheckoutViewSet, basename='checkout')

urlpatterns = [
    path('', include(router.urls)),
]
