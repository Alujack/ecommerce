from django.urls import path
from .views import create_order

urlpatterns = [
    path('create-order/def/', create_order, name='create_order'),
]
