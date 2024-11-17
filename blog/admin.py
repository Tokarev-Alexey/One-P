from django.contrib import admin
from .models import Post, Comment, Follow, Person

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Follow)

admin.site.register(Person)
