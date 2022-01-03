from workflow.models import Application, Company, Job
from workflow.serializers import ApplicationSerializer, CompanySerializer, JobSerializer
from workflow.permissions import IsManagerOrReadOnly
from rest_framework import generics, permissions, status
from rest_framework.response import Response


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


class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def list(self, request, *args, **kwargs):
        queryset = Application.objects.filter(applicant_id=request.user.id)
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
