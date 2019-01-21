from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('bookmark-detail', views.BookmarkDetailViewSet)

app_name = 'bookmark'

urlpatterns = [
    path('', include(router.urls))
]
