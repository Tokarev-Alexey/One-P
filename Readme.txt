Клонируем проект:

1.git clone git@github.com:Tokarev-Alexey/One-P.git
2.cd /One-P # заходим в папку с проектом

Запуск с докера:

1. docker build -t project .
2. docker run --rm -p 8000:8000 project

LOGIN: oneuser
PASSWORD: onepassword

Планировщик возможно проверить только в развернутом настольном варианте, запустив его в отдельном окне терминала.
База данных локальная, отдельную для контейнера не создавал.

Url'ы к API:

api/  - api-root
api/posts/  - все записи   только GET-list, POST-entry, HEAD, OPTIONS
api/posts/?author=<author_id> - сортировка записей по автору GET, POST, HEAD, OPTIONS
api/post/<pk> - одна запись по id записи GET, PUT, PATCH, HEAD, OPTIONS
api/comments/ - все комметарии GET, POST, HEAD, OPTIONS
api/comments/?post=<pk>  -комментарии одного поста GET, POST, HEAD, OPTIONS
api/api-auth/login/
api/api-auth/logout/
api/info/ - скачивание файла Statistic.txt

запуск  с nginx:
запускаем uwsgi в терминале pycharm:
uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=664

если нужно перезапускаем nginx:
sudo systemctl restart nginx