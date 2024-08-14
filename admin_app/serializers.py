from rest_framework import serializers
from base.models import CategoriesAdmin


class CategoriesAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesAdmin
        fields ="__all__"


