from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from workflow import views

urlpatterns = [
    path('companies', views.CompanyList.as_view(), name='companies-list'),
]
