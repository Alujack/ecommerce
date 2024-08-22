from django.urls import path
from .cart.order_cart import *
urlpatterns = [
    path('cart/<str:pk>/', get_cart_items, name="get_cart_by_user"),
    path('cart/create/<str:pk>/', add_cart_items, name="get_cart_by_user"),
    path('favourite/create/<str:pk>',
         add_favourite_items, name="fourite_by_user"),
    path('favourite/get/<str:pk>/', get_favourite_items, name="get_fav_by_user"),
]
