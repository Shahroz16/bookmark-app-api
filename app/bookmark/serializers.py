from rest_framework import serializers
from ..core import models


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """
    class Meta:
        model = models.Tag
        fields = ('user', 'name')
        read_only_fields = ('id',)


class BookmarkDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark detail model
    """

    class Meta:
        model = models.BookmarkDetail
        fields = ('user', 'name')
        read_only_fields = ('id',)


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark model
    """

    details = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=models.BookmarkDetail.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Bookmark
        field = ("id", "title", "url", "tags", "details")
        read_only_fields = ("id",)


class BookmarkFullDetailSerializer(serializers.ModelSerializer):

    details = BookmarkDetailSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
