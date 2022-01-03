from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from workflow.models import Application, Company, Job
from workflow.factories import ApplicationFactory, CompanyFactory, JobFactory, UserFactory
from workflow.contracts import UserTypes, JobTypes, JobContracts, JobModalities, ApplicationStatuses


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


class ApplicationListViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('application-list')

        company = CompanyFactory(jobs=None)
        self.job = JobFactory(company=company, applications=None)

        self.applicant = UserFactory(username='applicant', type=UserTypes.APPLICANT)
        self.data = {
            'applicant': self.applicant.id,
            'job': self.job.id,
            'description': 'Some description here',
            'status': ApplicationStatuses.APPLIED
        }

    def test_unauthenticated_users_cannot_apply_to_a_job(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_applicants_can_apply_to_a_job(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().description, 'Some description here')

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
