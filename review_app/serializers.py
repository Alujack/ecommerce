from rest_framework import serializers
from base.models import UserReview

class UserReviewSerializers(serializers.ModelSerializer):
    class Meta:
        models = UserReview
        fields ="__all__"
