from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create(**params)


class TestPublicUserApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_able_to_create_user(self):
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_password_too_short(self):
        payload = {"email": "test@example.com", "password": "pw", "name": "test user"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)
