
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, UserReview
api_view(['POST'])
def create_comment(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user
    comment = UserWarning.objects.get( )
    comment = UserReview.get_or_create(
        user= user,
        product=product,
        comment=comment,
    )
