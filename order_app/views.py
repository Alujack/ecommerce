from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from base.models import *
from .serializers import *


@api_view(['GET'])
def get_order_history(request, pk):
    user = User.objects.get(id=pk)
    orders = OrderHistory.objects.filter(user=user)
    serializers = OrderHistorySerializer(orders, many=True)
    if serializers:
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
