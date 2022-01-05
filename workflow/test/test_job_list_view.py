from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Job
from workflow.factories import CompanyFactory
from workflow.contracts import JobTypes, JobContracts, JobModalities
from authentication.contracts import UserTypes
from authentication.factories import UserFactory


class JobListViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('job-list')
        self.company = CompanyFactory(jobs=None)
        self.data = {
            'company': self.company.id,
            'title': 'Data Engineer',
            'category': 'Engineering',
            'description': 'Some description',
            'contract': JobContracts.PERMANENT,
            'type': JobTypes.FULL_TIME,
            'modalities': JobModalities.HYBRID
        }

    def test_unauthenticated_users_can_list_jobs(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applicants_cannot_create_a_job(self) -> None:
        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Job.objects.count(), 0)

    def test_managers_can_create_a_job(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Job.objects.get().title, 'Data Engineer')