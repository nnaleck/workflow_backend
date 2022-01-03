from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Company
from workflow.factories import CompanyFactory, UserFactory
from workflow.contracts import UserTypes


class CompanyDetailViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.company = CompanyFactory()
        self.url = reverse('company-detail', kwargs={'pk': self.company.id})
        self.data = {
            'name': 'Updated company'
        }

    def test_unauthenticated_users_and_applicants_can_retrieve_a_company(self) -> None:
        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)

        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)

    def test_applicants_cannot_update_and_destroy_a_company(self) -> None:
        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Company.objects.get().name, 'Updated company')

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Company.objects.count(), 1)

    def test_managers_can_update_a_company(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get().name, 'Updated company')

    def test_managers_can_delete_a_company(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)