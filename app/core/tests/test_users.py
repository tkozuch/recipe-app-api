from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    def test_able_to_create_user(self):
        email = "person@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        emails = [
            ("test@Example.com", "test@example.com"),
            ("Test2@Example.com", "Test2@example.com"),
            ("TEST3@example.com", "TEST3@example.com"),
            ("TEST4@EXAMPLE.com", "TEST4@example.com"),
            ("test5@example.COM", "test5@example.com"),
        ]

        for email, sanitized in emails:
            user = get_user_model().objects.create_user(
                email=email, password="testpass"
            )

            self.assertEqual(user.email, sanitized)

    def test_email_required(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="testpassword")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@example.com", password="test123"
        )

        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("test123"))
