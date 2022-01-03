from rest_framework import serializers
from workflow.models import Application, Company, Job, User


class JobSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Job
        fields = [
            'id', 'company', 'title', 'description',
            'contract', 'type', 'modalities',
            'created_at', 'published_at', 'closed_at'
        ]
        read_only_fields = ['created_at']


class CompanySerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'jobs', 'created_at']
        read_only_fields = ['created_at']


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'job', 'description', 'attachments', 'status', 'created_at']
        read_only_field = ['created_at']