from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategoriesAdminSerializer

api_view(['GET'])
def create_admin_category(request):
    data = request.data
    serializers = CategoriesAdminSerializer(data=data)
    if serializers.is_valid():
         return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
