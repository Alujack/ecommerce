from django.urls import path, include
from .views import category_management

urlpatterns = [
    path('category/', category_management, name="category-list"),
    path('category/<str:pk>', category_management , name="category-list")
]
