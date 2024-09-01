from django.urls import path
from .views import ProductListView, search_products

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('search_products/', search_products, name="search_products"),
    path('product/list/< str:pk>/', )
]
