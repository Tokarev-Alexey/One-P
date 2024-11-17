from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import jwt


class Person(User):
    objects = None
    token = models.CharField(max_length=200)

    class Meta:
        proxy = True
        ordering = ('first_name',)

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        self.token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return self.token


class Post(models.Model):
    objects = None
    id = models.CharField
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)  # == order_by('created_date')

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Follow(models.Model):
    objects = None
    # пользователь, который подписывается
    user = models.ForeignKey(Person, related_name='following', on_delete=models.CASCADE)
    # пользователь, на которого подписывются
    author = models.ForeignKey(Person, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return '{} подписан на {}'.format(self.user, self.author)
