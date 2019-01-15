from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models

def sample_user(email='test@test.com', password='test1'):
    """
    Create a sample user
    """

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    """
    Test cases for UserModel
    """

    def test_create_user_with_email_successful(self):
        
        email = "shahrozTest@test.com"
        password = "Testpass122"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for new user is normalized
        """

        email = "test2@TEST.COM"

        user = get_user_model().objects.create_user(
            email=email,
            password='testt1111'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating new user with no email raises error
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test122")

    def test_super_user_create(self):
        """
        Test creating a new superuser
        """

        user = get_user_model().objects.create_superuser("super@test.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
        Test the tag string representation
        """

        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Food"
        )

        self.assertEqual(str(tag), tag.name)