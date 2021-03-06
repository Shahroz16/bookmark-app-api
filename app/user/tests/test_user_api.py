from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API public
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):

        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'testt'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {'email': 'test@test.com', 'password': 'test123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_token_for_user(self):
    #     payload = {'email': 'test11@test.com', 'password': 'test123'}
    #     create_user(**payload)

    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        payload = {'email': 'test@test.com', 'password': 'test123'}
        create_user(**payload)

        res = self.client.post(
            TOKEN_URL, {'email': 'test@test.com', 'password': 'test12'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):

        res = self.client.post(TOKEN_URL, {'email': "test", 'password': ""})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test to check authorization is required
        """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    class PrivateUserApiTests(TestCase):

        def setUp(self):

            self.user = create_user(
                email='shahroz@test.com',
                password='testt1',
                name='shahroz'
            )

            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

        def test_retrieve_profile(self):

            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data,
                             {'name': self.user.name,
                                 'email': self.user.email})

        def test_user_profile_update(self):

            payload = {'name': 'hollaaaa', 'password' : 'password112'}

            res = self.client.patch(ME_URL, payload)
            
            self.user.refresh_from_db()
            self.assertEqual(self.user.name, payload['name'])
