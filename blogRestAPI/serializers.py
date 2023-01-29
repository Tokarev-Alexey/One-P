from rest_framework import serializers
from blog.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'body', 'created', 'updated')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_date', 'published_date', 'comments')