from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Job
from workflow.factories import CompanyFactory, JobFactory
from workflow.contracts import JobTypes, JobContracts, JobModalities
from authentication.contracts import UserTypes
from authentication.factories import UserFactory


class JobDetailViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        company = CompanyFactory(jobs=None)
        self.job = JobFactory(company=company)
        self.url = reverse('job-detail', kwargs={'pk': self.job.id})
        self.data = {
            'company': self.job.company_id,
            'title': 'Updated job',
            'category': 'Engineering',
            'description': 'Some description',
            'contract': JobContracts.INTERNSHIP,
            'type': JobTypes.FULL_TIME,
            'modalities': JobModalities.HYBRID
        }

    def test_unauthenticated_users_and_applicants_can_retrieve_a_job(self) -> None:
        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.job.title)

        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.job.title)

    def test_applicants_cannot_update_and_destroy_a_job(self) -> None:
        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Job.objects.get().title, 'Updated job')
        self.assertNotEqual(Job.objects.get().contract, JobContracts.INTERNSHIP)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Job.objects.count(), 1)

    def test_managers_can_update_a_job(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.get().title, 'Updated job')
        self.assertEqual(Job.objects.get().contract, JobContracts.INTERNSHIP)

    def test_managers_can_delete_a_job(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Job.objects.count(), 0)
