from django.urls import path
from .views import ProductListView, search_products, product_relate,  get_filter_products

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('search_products/', search_products, name="search_products"),
    path('product/list/<str:pk>/', product_relate, name="product_relate"),
    path('get-filter-price/', get_filter_products, name=" get_filter_products")
]
