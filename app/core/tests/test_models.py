from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "funtimesdude@living.com"
        password = "HeyLookIt'sAnUnsecurredPassword!"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONdonAPPDudE.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Test creating user with no email raises an error"""
        # this test should raise a ValueError exception
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,
                                                 "Another Sweet Password")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'heydude@yo.com',
            'NiftyPassword'
        )
        # is_superuser function is included as a part of the permissions mixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
