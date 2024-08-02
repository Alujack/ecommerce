from django.urls import path, include
from .views import category_management, ProductDetailView, get_one_category_and_create_detail_variations

urlpatterns = [
    path('category/', category_management, name="category-list"),
    path('category/<str:pk>/', category_management , name="category-list"),
    path('category/<str:pk>/detail/',
         get_one_category_and_create_detail_variations, name="category-list"),
    path('products/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
]
