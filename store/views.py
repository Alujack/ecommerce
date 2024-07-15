from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from base.models import Store, Address
from api.serializers import StoreSerializer

User = get_user_model()


@api_view(['POST'])
def create_or_update_store(request):
    seller_data = request.data.get('seller')
    address_data = request.data.get('address')
    name = request.data.get('name')

    # Check if the user exists
    try:
        user = User.objects.get(email=seller_data['email'])
    except User.DoesNotExist:
        return Response({'seller': {'email': 'User does not exist'}}, status=status.HTTP_400_BAD_REQUEST)

    # Update or create address
    address, _ = Address.objects.update_or_create(**address_data)

    # Update or create store
    store, created = Store.objects.update_or_create(
        seller=user,
        address=address,
        defaults={'name': name}
    )

    return Response(StoreSerializer(store).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
