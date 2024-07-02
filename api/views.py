from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import *
from .serializers import *


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateStoreView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class PostProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

