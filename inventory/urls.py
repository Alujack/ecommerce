from django.urls import path
from .views import *


urlpatterns = [
    path('product/', get_product_by_category, name="get_product"),
    path('sub_categories/', get_sub_categories, name="get_sub_catgories"),
    path('parent_categories/', get_parents_categories,
         name="get_parents_catgories"),
    path('new_arrival/', get_new_arrival_products,
         name="get_new_arrival_products"),
    path('category/new_arrival/', get_new_arrival_products_in_category,
         name="get_new_arrival_products_in_category"),
    path('category/contain/products/', get_cat_contain_product,
         name="get_cat_contain_product"),

]
