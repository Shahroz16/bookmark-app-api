from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .core.models import BookmarkDetail
from bookmark.serializers import BookmarkDetailSerializer

BOOKMARK_DETAILS_URL = reverse('bookmakr:bookmark-detail-list')


class PublicBookmarkDetailsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(BOOKMARK_DETAILS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookmarkDetailsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test@test.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_bookmark_details(self):
        
        BookmarkDetail.objects.create(user=self.user, name='Salt')
        BookmarkDetail.objects.create(user=self.user, name='Ploo')

        res = self.client.get(BOOKMARK_DETAILS_URL)

        bookmarkDetails = BookmarkDetail.objects.all().order_by('-name')

        serializer = BookmarkDetailSerializer(bookmarkDetails, many=True)
        self.assertEquals(res.data, serializer.data)

    def test_bookmark_details_limited_to_user(self):

        user2 = get_user_model().object.create_user(
            'test2@test.com',
            'testt22')

        BookmarkDetail.objects.create(user=self.user, name='Salt')
        detail = BookmarkDetail.objects.create(user=self.user2, name='JOIL')

        res = self.client.get(BOOKMARK_DETAILS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], detail.name)

    def test_create_bookmark_detail(self):

        payload = {'name': 'Coco'}

        self.client.post(BOOKMARK_DETAILS_URL, payload)

        exists = BookmarkDetail.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)