from rest_framework import serializers
from core.models import Tag, BookmarkDetail


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """
    class Meta:
        model = Tag
        fields = ('user', 'name')
        read_only_fields = ('id',)


class BookmarkDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark detail model
    """

    class Meta:
        model = BookmarkDetail
        fields = ('user', 'name')
        read_only_fields = ('id',)