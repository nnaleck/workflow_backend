from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Application
from workflow.factories import ApplicationFactory, CompanyFactory, JobFactory, UserFactory
from workflow.contracts import UserTypes, ApplicationStatuses


class ApplicationDetailViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.company = CompanyFactory(jobs=None)
        self.job = JobFactory(company=self.company, applications=None)

        self.applicant = UserFactory(username='applicant', type=UserTypes.APPLICANT)
        self.application = ApplicationFactory(
            applicant=self.applicant,
            job=self.job,
        )

        self.url = reverse('application-detail', kwargs={'pk': self.application.id})

        self.data = {
            'applicant': self.applicant.id,
            'job': self.job.id,
            'description': 'Updated description',
            'status': ApplicationStatuses.APPLIED
        }

    def test_applicants_can_retrieve_their_application(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applicants_can_only_retrieve_their_application(self):
        # Creating an application that belongs to another applicant
        application = ApplicationFactory(
            job=self.job
        )

        self.client.force_authenticate(user=self.applicant)

        response = self.client.get(reverse('application-detail', kwargs={'pk': application.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_users_cannot_retrieve_an_application(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_users_cannot_perform_update_and_destroy_actions(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_managers_can_delete_an_application(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)

    def test_managers_can_update_an_application_status(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.patch(self.url, {'status': ApplicationStatuses.IN_REVIEW})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.get().status, ApplicationStatuses.IN_REVIEW)

    def test_applicants_cannot_delete_their_application(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Application.objects.count(), 1)

    def test_applicants_cannot_update_their_application_status(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.patch(self.url, {'status': ApplicationStatuses.IN_REVIEW})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Application.objects.get().status, ApplicationStatuses.IN_REVIEW)
