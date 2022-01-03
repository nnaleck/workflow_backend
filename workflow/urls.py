from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from workflow import views

urlpatterns = [
    path('companies', views.CompanyList.as_view(), name='company-list'),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name='company-detail'),
    path('jobs', views.JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>', views.JobDetail.as_view(), name='job-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
