from django.urls import path
from .cart.order_cart import *
urlpatterns = [
    path('cart/<str:pk>/',get_cart_items, name="get_cart_by_user" ),
]
