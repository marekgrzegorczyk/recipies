from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')  # /api/user/create
TOKEN_URL = reverse('user:token')  # /api/user/token
ME_URL = reverse('user:me')  # /api/user/me

user_details = {
    'email': 'testtest@examplee.com',
    'password': 'testpass',
    'name': 'Test name'
}

payload = {
    'email': user_details['email'],
    'password': user_details['password']
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        res = self.client.post(CREATE_USER_URL, user_details)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=user_details['email'])

        self.assertTrue(user.check_password(user_details['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        create_user(**user_details)
        res = self.client.post(CREATE_USER_URL, user_details)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        user_details['password'] = 'pw'

        res = self.client.post(CREATE_USER_URL, user_details)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=user_details['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        create_user(**user_details)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(**user_details)
        payload['password'] = 'wrong'
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        updated_payload = {
            'name': 'new name',
            'password': 'newpassword'
        }

        res = self.client.patch(ME_URL, updated_payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, updated_payload['name'])
        self.assertTrue(self.user.check_password(updated_payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
