from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase
from user.tests.test_user_api import user_details


class TestUserModel(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@test.test'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='testpassword')
            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None,
                                                 password='testpassword')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpassword'
        )
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(**user_details)

        recipe = models.Recipe.objects.create(
            user=user,
            title='Recipe',
            time_minutes=5,
            price=Decimal(5.50),
            description='Test description'
        )

        self.assertEqual(str(recipe), recipe.title)
