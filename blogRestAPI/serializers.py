from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'body', 'created', 'updated')


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     author = serializers.CharField()
#     title = serializers.CharField(max_length=200)
#     text = serializers.CharField()
#     created_date = serializers.DateTimeField(read_only=True)
#     published_date = serializers.DateTimeField(read_only=True)
#     def create(self, validated_data):
#         return Post.objects.create(**validated_data)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_date', 'published_date')

class PostSerializerOneObject(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_date', 'published_date', 'comments')