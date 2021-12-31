from workflow.models import Company, Job
from workflow.serializers import CompanySerializer, JobSerializer
from workflow.permissions import IsManagerOrReadOnly
from rest_framework import generics, permissions


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