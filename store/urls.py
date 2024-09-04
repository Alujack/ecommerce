from django.urls import path
from .views import *
from .customer_order import *
urlpatterns = [
    path('manage/stores/', store_view, name='store_view'),
    path('manage/stores/<str:pk>/', store_view, name='store_view_update'),
    path('product/publishing/<str:pk>/',
         get_publish_by_store, name="get_publish"),
    path('product/draft/<str:pk>/',
         get_draft_by_store, name="get_draft"),
    path('customer/list/<str:pk>/', get_cutomers_by_store, name="customer_list"),
    path('product/detail/<str:pk>/', get_product_detail, name="product_deatil"),
    path('search/category/', search_categories, name="search_categories"),
    path('category/save/<str:pk>/', save_store_category, name="save_category"),
    path('category/save/<str:pk>', save_store_category, name="save_category"),
    path('customer/order-list', get_order_line, name="get_order_line"),
]
