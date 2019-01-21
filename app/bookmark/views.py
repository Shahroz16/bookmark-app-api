from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, BookmarkDetail
from .serializers import TagSerializer, BookmarkDetailSerializer


class BaseBookmarkAttrViewSets(viewsets.GenericViewSet, mixins.ListModelMixin,
                               mixins.CreateModelMixin):
    """
    Base viewset for user ownerd bookmark
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseBookmarkAttrViewSets):
    """
    Manage tags in the db
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BookmarkDetailViewSet(BaseBookmarkAttrViewSets):
    """
    Manage bookmark details in the db
    """
    queryset = BookmarkDetail.objects.all()
    serializer_class = BookmarkDetailSerializer
