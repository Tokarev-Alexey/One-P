from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from django.http import FileResponse

from .models import Post, Comment
from blogRestAPI.serializers import PostSerializer, PostSerializerOneObject, CommentSerializer


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
            return self.queryset # == return Post.objects.all().order_by('-published_date')

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