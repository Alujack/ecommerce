from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  create_or_update_store



urlpatterns = [
    path('store/create_or_update/', create_or_update_store,
         name='create_or_update_store'),
]
