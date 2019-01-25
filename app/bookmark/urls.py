from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, BookmarkDetailViewSet


router = DefaultRouter()
router.register('tag', TagViewSet)
router.register('detail', BookmarkDetailViewSet)

app_name = 'bookmark'

urlpatterns = [
    path('', include(router.urls))
]
