from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Company, Job
from workflow.factories import CompanyFactory, JobFactory, UserFactory
from workflow.contracts import UserTypes, JobTypes, JobContracts, JobModalities


class CompanyListViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('company-list')
        self.data = {
            'name': 'Company',
            'address': None
        }

    def test_unauthenticated_users_can_only_list_companies(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applicants_cannot_create_a_company(self) -> None:
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

        applicant = UserFactory(username='applicant')
        self.client.force_authenticate(user=applicant)

        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
