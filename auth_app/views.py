# In your Django app's views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()


@csrf_exempt
def create_or_update_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user, created = User.objects.update_or_create(
            email=data['email'],
            first_name = data['name'],
            last_name=data['name'],
            defaults={'username': data['name']}
        )
        return JsonResponse({'created': created})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return JsonResponse({'message': 'This is a protected view'})
