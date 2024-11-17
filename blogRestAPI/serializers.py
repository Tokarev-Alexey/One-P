from rest_framework import serializers
from .models import Post, Comment, User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( 'id', 'username', 'password', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'body', 'created', 'updated')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_date', 'published_date')

class PostSerializerOneObject(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_date', 'published_date', 'comments')
