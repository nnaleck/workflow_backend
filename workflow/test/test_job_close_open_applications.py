from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from authentication.factories import UserFactory
from authentication.contracts import UserTypes
from workflow.factories import CompanyFactory, JobFactory
from workflow.models import Job
from django.utils import timezone


class JobCloseOpenApplicationsTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.company = CompanyFactory(jobs=None)
        self.job = JobFactory(company=self.company)
        self.applicant = UserFactory(username='applicant', type=UserTypes.APPLICANT)
        self.manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.url = reverse('job-close', kwargs={'pk': self.job.id})

    def test_unauthenticated_users_cannot_close_job_applications(self):
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Job.objects.get().closed_at, None)

    def test_applicants_cannot_close_job_applications(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Job.objects.get().closed_at, None)

    def test_managers_can_close_job_applications(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Job.objects.get().closed_at, None)

    def test_managers_can_open_job_applications_if_its_already_closed(self):
        self.job.delete()
        self.job = JobFactory(company=self.company, closed_at=timezone.now())

        self.client.force_authenticate(user=self.manager)

        response = self.client.patch(reverse('job-close', kwargs={'pk': self.job.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.get().closed_at, None)
