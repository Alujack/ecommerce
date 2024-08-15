from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import ProductCategory
from .serializers import ProductCategorySerializer

User = get_user_model()


@api_view(['GET', 'POST', 'DELETE'])
def category_management(request, pk=None):

    if request.method == 'GET':
        categories = ProductCategory.objects.all()
        if categories:
            serializer = ProductCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        category_data = request.data
        serializer = ProductCategorySerializer(data=category_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            category = ProductCategory.objects.get(id=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
