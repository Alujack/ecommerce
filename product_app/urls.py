from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import category_management, ProductViewSet, get_one_category_and_create_detail_variations, create_product

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('category/', category_management, name="category-list"),
    path('category/<str:pk>/', category_management, name="category-list"),
    path('category/<str:pk>/detail/',
         get_one_category_and_create_detail_variations, name="category-list"),
    path('', include(router.urls)),
    path('productss/', create_product, name='product'),
]
