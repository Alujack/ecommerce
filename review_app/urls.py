from django.urls import path
from .views import create_comment, list_comments

urlpatterns = [
    path('comments/create/', create_comment, name='create_comment'),
    path('comments/', list_comments, name='list_comments'),
]
