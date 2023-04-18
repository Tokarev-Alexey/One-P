from rest_framework import routers
from django.urls import path, include

from . import views
from .views import PostViewSet, CommentViewSet, PostViewSetDetail

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'post', PostViewSetDetail)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/info/', views.load_statistic, name='loadstatistic'),
    ]