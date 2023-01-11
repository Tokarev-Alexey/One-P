from blog.models import Post, Comment
from rest_framework import viewsets
from blog.RestAPI.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.query_params.get('author'):
            make = self.request.query_params.get('author')
            return Post.objects.filter(author=make)
        else: return self.queryset # == return Post.objects.all().order_by('-published_date')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post')
    serializer_class = CommentSerializer
