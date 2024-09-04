from rest_framework import serializers
from base.models import UserReview


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        models = UserReview
        fields = "__all__"
    # If you want to return the username instead of the ID
    user = serializers.StringRelatedField()
    # If you want to return the product name instead of the ID
    product = serializers.StringRelatedField()
