from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from authentication.models import User


class RegisterViewTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {
            'email': 'admin@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'secret_1234_56',
            'password_confirmation': 'secret_1234_56'
        }

        self.url = reverse('auth-register')

    def test_registration_data_must_be_valid(self):
        self.data['email'] = 'invalid'
        self.data['password_confirmation'] = 'not_secret'

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_is_successful_with_valid_data(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'admin@test.com')
        self.assertEqual(User.objects.get().username, 'john_doe')
