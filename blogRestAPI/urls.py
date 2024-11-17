from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *
from .views import PostViewSet, CommentViewSet, PostViewSetDetail

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'post', PostViewSetDetail, basename='something-unique')
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
#    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('info/', load_statistic, name='loadstatistic'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('reg/', CreateUserView.as_view(), name='create_user'),
]

