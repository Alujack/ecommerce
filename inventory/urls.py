from django.urls import path, include
from .views import *


urlpatterns = [
    path('product/<str:pk>/',get_product_by_category, name="get_product")
]
