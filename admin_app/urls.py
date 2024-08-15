from django.urls import path
from .views import *
urlpatterns = [
    path('create/categories/', category_management, name="category_management"),
    path('create/categories/<str:pk>/',
         category_management, name="category"),
]
