from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from base.models import Store
from api.serializers import StoreSerializer

User = get_user_model()


@api_view(['GET', 'POST', 'PUT'])
def store_view(request, pk=None):
    if request.method == 'GET':
        try:
            store = Store.objects.get(seller=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            user = User.objects.get(id=pk)
            request.data['seller'] = pk
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not pk:
            return Response({'error': 'Store ID is required for update'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('seller')
        if not user_id:
            return Response({'error': 'Seller ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            request.data['seller'] = user.id
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
