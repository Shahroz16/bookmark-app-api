from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from .. import serializers

TAG_URL = reverse('bookmark:tag-list')


class PublicTagsAPITests(TestCase):
    """
    Test the publically availble Tags
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required for tags
        """

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateTagsAPITests(TestCase):
    """
    Test the authorized user tags API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test1'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):

        Tag.objects.create(user=self.user, name='Food')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = serializers.TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):

        user2= get_user_model().objects.create_user(
            'test2@test.com',
            'test2'
        )

        Tag.objects.create(user=user2, name="Fruity")

        tag = Tag.objects.create(user=self.user, name="Choco")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)