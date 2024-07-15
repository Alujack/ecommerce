from django.urls import path
from .views import MyTokenObtainPairView, login

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', login, name='login'),
]
