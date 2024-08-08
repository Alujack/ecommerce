from django.urls import path
from .views import store_view, get_publish_by_store
urlpatterns = [
    path('manage/stores/', store_view, name='store_view'),
    path('manage/stores/<str:pk>/', store_view, name='store_view_update'),
    path('product/publishing/<str:pk>/', get_publish_by_store, name="get_publish")
]
