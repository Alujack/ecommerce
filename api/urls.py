from django.urls import path
from .views import CreateUserView, CreateStoreView, PostProductView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('create-store/', CreateStoreView.as_view(), name='create-store'),
    path('post-product/', PostProductView.as_view(), name='post-product'),
]
