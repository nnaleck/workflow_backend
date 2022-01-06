from workflow.models import Application, Company, Job
from workflow.serializers import ApplicationSerializer, CompanySerializer, JobSerializer
from workflow.permissions import IsManagerOrReadOnly, IsManagerOrOwnerOfApplication
from authentication.contracts import UserTypes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsManagerOrReadOnly
    ]


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsManagerOrReadOnly
    ]


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsManagerOrReadOnly
    ]


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsManagerOrReadOnly
    ]

    def patch(self, request, *args, **kwargs):
        job = self.get_object()

        if job.published_at:
            job.published_at = None
        else:
            job.published_at = timezone.now()

        job.save()

        return Response({}, status=status.HTTP_200_OK)


class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def list(self, request, *args, **kwargs):
        queryset = Application.objects.filter(applicant_id=request.user.id)

        if request.user.type == UserTypes.MANAGER:
            queryset = self.get_queryset()

        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsManagerOrOwnerOfApplication
    ]
