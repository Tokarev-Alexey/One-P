from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.http import FileResponse
from rest_framework.generics import CreateAPIView
from .models import Post, Comment, User
from blogRestAPI.serializers import PostSerializer, PostSerializerOneObject, CommentSerializer, UserSerializer
from rest_framework import permissions

from .renderers import UserJSONRenderer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.query_params.get('author'):
            make = self.request.query_params.get('author')
            return Post.objects.filter(author=make).order_by('-published_date')
        else:
            return self.queryset  # == return Post.objects.all().order_by('-published_date')


class PostViewSetDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializerOneObject


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post')
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request.query_params.get('post'):
            make = self.request.query_params.get('post')
            return Comment.objects.filter(post=make).order_by('post')
        else:
            return self.queryset


def load_statistic(response):
    response = FileResponse(open('Statistic.csv', 'rb'))
    return response
