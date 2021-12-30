from rest_framework import serializers
from workflow.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'created_at']
        read_only_fields = ['created_at']