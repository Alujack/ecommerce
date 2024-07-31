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
        user_id = request.query_params.get('seller')
        if user_id:
            stores = Store.objects.filter(seller__id=user_id)
        serializer = StoreSerializer(stores)
        return Response(serializer.data)

    elif request.method == 'POST':
       
        try:
            user = User.objects.get(id=pk)
            if user:
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

        
        try:
            user = User.objects.get(id=user_id)
            request.data['seller'] = user.id
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


