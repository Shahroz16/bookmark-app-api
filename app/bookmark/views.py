from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, BookmarkDetail
from .serializers import TagSerializer, BookmarkDetailSerializer


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """
    Manage tags in the db
    """

    authentical_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Create a new tag
        """

        serializer.save(user=self.request.user)


class BookmarkDetailViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Manage bookmark details in the db
    """

    authentical_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BookmarkDetail.objects.all()
    serializer_class = BookmarkDetailSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')