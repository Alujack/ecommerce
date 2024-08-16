from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .category import *
from .product import *
from .post import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'variations', VariationsViewSet)
router.register(r'variation-options', VariationOptionViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-items', ProductItemViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
    path('category/', category_management, name="category-list"),
    path('category/<str:pk>/', category_management, name="category-list"),
    path('category/<str:pk>/detail/',
         get_one_category_and_create_detail_variations, name="category-list"),
    path('create/', create_product, name='product'),
    path('category/variations/<str:pk>/', get_variations_use_category,
         name='get_variation_use_category'),
    path('category/product/<str:pk>/',
         get_product_by_category, name='get_product'),
    path('store/<str:pk>/product/', get_product_by_store, name="product_in_store"),
    path('store/product/delete/', delete_product, name="delete_product"),
    path('store/product/post/<str:pk>/',  post_product, name="post_product"),
    path('store/product/get/<str:pk>/', get_product_by_id, name="product_get"),
    path('store/category/get/<str:pk>/', get_categories_by_product,
         name="get_category_by_product"),
    path('store/category/variations/get/<str:pk>/',  get_variations_by_category,
         name="get_variations_by_category"),
    path('store/options/get/<str:pk>/', get_options_by_variation,
         name="get_options_by_variation"),
    path('store/category/variations/options/get/<str:pk>/', get_variations_and_Options_id,
         name="get_options_and_variation_by_category"),
    path('store/product/publish/<str:pk>/', publish_product, name="publish"),
    path('store/product/draft/<str:pk>/', draft_product, name="draft")

]
