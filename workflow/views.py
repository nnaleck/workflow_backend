from workflow.models import Company
from workflow.serializers import CompanySerializer
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
