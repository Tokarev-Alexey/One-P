import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import csv
from blog.models import Post



def period():
    with open('Statistic.csv', 'w', newline='') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        linewriter.writerow(['author', 'count_entries', 'anoc, %']) # anoc - average number of comments
        list = Post.objects.all()
        authors = {}
        for i in list:
            anoc = 0
            posts_author = Post.objects.filter(author_id=i.author_id)
            for j in posts_author:
                comments = j.comments.filter(active=True).count()
                anoc += comments
            anoc = anoc / posts_author.count()
            linewriter.writerow([str(i.author),  posts_author.count(), round(anoc, 1)])
            anoc = 0

scheduler = BackgroundScheduler()
scheduler.add_job(period, 'interval', seconds=1)

scheduler.start()

while True:
    sleep(1)