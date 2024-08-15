from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('auth_app.urls')),
    path('store/', include('store.urls')),
    path('product/', include('product_app.urls')),
    path('admin_manage/', include('admin_app.urls')),

]
