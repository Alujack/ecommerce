from django.urls import path
from .views import *
from .best_seller import get_bestseller_in_cat
from .new_arrival import get_new_in_cat


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
    path('best-seller/', get_bestseller_in_cat, name="get_bestseller_in_cat"),
    path('new-arrival/', get_new_in_cat, name="get_new_in_cat"),

]
