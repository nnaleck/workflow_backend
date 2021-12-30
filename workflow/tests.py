from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Company
from workflow.factories import UserFactory
from workflow.contracts import UserTypes


class CompanyListViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('companies-list')
        self.data = {
            'name': 'Company',
            'address': None
        }

    def test_unauthenticated_users_can_only_list_companies(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_managers_cannot_create_a_company(self) -> None:
        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Company.objects.count(), 0)

    def test_managers_can_create_a_company(self) -> None:
        manager = UserFactory(username='manager', type=UserTypes.MANAGER)
        self.client.force_authenticate(user=manager)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'Company')