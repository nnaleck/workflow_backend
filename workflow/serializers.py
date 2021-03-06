from rest_framework import serializers
from workflow.models import Application, Company, Job
from authentication.models import User


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
    resume = serializers.FileField(
        max_length=None,
        allow_null=True,
        required=False,
        use_url=True
    )

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'job', 'description', 'resume', 'status', 'created_at']
        read_only_field = ['created_at']

    def validate(self, attrs):
        if 'job' in attrs and not attrs['job'].published_at:
            raise serializers.ValidationError({
                'job': 'You cannot apply to a job that is not published yet.'
            })

        if 'job' in attrs and attrs['job'].closed_at:
            raise serializers.ValidationError({
                'job': 'The job that you are applying for is no longer accepting applications.'
            })

        return attrs
