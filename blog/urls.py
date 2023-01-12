from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.delete, name='delete'),
    path('post/author/<int:id>/<value>/', views.author_list, name='author_list'),
    path('register/', views.register, name='register'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile, name='profile'),

]
