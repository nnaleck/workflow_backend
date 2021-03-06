from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from workflow.models import Application
from workflow.factories import ApplicationFactory, CompanyFactory, JobFactory
from workflow.contracts import ApplicationStatuses
from authentication.contracts import UserTypes
from authentication.factories import UserFactory


class ApplicationListViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('application-list')

        self.company = CompanyFactory(jobs=None)
        self.job = JobFactory(
            company=self.company,
            applications=None,
            published_at=timezone.now()
        )

        self.applicant = UserFactory(username='applicant', type=UserTypes.APPLICANT)
        self.data = {
            'applicant': self.applicant.id,
            'job': self.job.id,
            'description': 'Some description here',
            'status': ApplicationStatuses.APPLIED
        }

    def test_unauthenticated_users_cannot_apply_to_a_job(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_applicants_can_apply_to_a_job(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().description, 'Some description here')

    def test_managers_cannot_apply_to_a_job(self):
        self.client.force_authenticate(user=UserFactory(username='manager', type=UserTypes.MANAGER))

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Application.objects.count(), 0)

    def test_applicants_cannot_apply_to_an_unpublished_job(self):
        self.job = JobFactory(
            company=self.company,
            applications=None,
            published_at=None
        )

        self.client.force_authenticate(user=self.applicant)

        self.data['job'] = self.job.id

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)

    def test_applicants_cannot_apply_to_a_job_that_does_not_accept_applications(self):
        self.job = JobFactory(
            company=self.company,
            applications=None,
            published_at=timezone.now(),
            closed_at=timezone.now()
        )

        self.client.force_authenticate(user=self.applicant)

        self.data['job'] = self.job.id

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)

    def test_applicants_can_view_their_applications(self):
        ApplicationFactory(
            applicant=self.applicant,
            job=self.job
        )

        self.client.force_authenticate(user=self.applicant)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_applicants_can_only_view_their_own_applications(self):
        # Creating an application for a different candidate and for the same job
        ApplicationFactory(job=self.job)

        self.client.force_authenticate(user=self.applicant)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])