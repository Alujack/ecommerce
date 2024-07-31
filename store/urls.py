from django.urls import path
from .views import store_view
urlpatterns = [
    path('manage/stores/', store_view, name='store_view'),
    path('manage/stores/<str:pk>/', store_view, name='store_view_update'),
]
