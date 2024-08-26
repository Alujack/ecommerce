from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from base.models import *


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class BankInformationViewSet(viewsets.ModelViewSet):
    queryset = BankInformation.objects.all()
    serializer_class = BankInformationSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class CheckoutViewSet(viewsets.ViewSet):
    serializer_class = CheckoutSerializer

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                'status': 'Order placed successfully',
                'order_id': order.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
