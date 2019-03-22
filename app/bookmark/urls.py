from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, BookmarkDetailViewSet, BookmarkViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('details', BookmarkDetailViewSet)
router.register('bookmarks', BookmarkViewSet)

app_name = 'bookmark'

urlpatterns = [
    path('', include(router.urls))
]
