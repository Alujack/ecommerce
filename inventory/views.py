
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import *
from .serializers import *
User = get_user_model()

@api_view(['GET'])
def get_product_by_category(request, pk):
    try:
        category = Category.objects.get(id=pk)  
        products = Product.objects.filter(categories=category)
        serializers = ProductSerializer(data=products,many=True)
        if serializers.is_valid():
            return Response(serializers.data, status= status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_404_NOT_FOUND)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

