from django.urls import path
from .cart.order_cart import *
from .views import *
urlpatterns = [
    path('cart/<str:pk>/', get_cart_items, name="get_cart_by_user"),
    path('cart/create/<str:pk>/', add_cart_items, name="get_cart_by_user"),
    path('favourite/create/<str:pk>/',
         add_favourite_items, name="fourite_by_user"),
    path('favourite/get', get_favourite_items, name="get_fav_by_user"),
    path('favourite/delete', delete_favourite, name="delete_fav"),
    path('cart/delete', delete_cart, name="delete_cart"),
    path('cart/delete/all', delete_all_cart, name="delete_all_cart"),
    path('order/<str:pk>/', get_order_history, name="get_order_history"),
 

]
