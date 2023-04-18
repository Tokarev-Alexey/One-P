import csv
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler

from blog.models import Post


print('The scheduler is running! It\'s Ok!' + '\n' + 'To stop, click <Ctrl + C>')
def my_job():
    with open('Statistic.csv', 'w', newline='') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        linewriter.writerow(['author', 'count_entries', 'anoc, %']) # anoc - average number of comments
        list = Post.objects.all()
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
scheduler.add_job(my_job, 'interval', seconds=5)

scheduler.start()

while True:
    sleep(1)

# ПРОСТО ВДРУГ ПОНАДОБИТСЯ

# import logging
# from django.conf import settings
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from django_apscheduler import util

# logger = logging.getLogger(__name__)

# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#   DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#   help = "Runs APScheduler."
#
#   def handle(self, *args, **options):
#     scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     scheduler.add_job(
#       my_job,
#       trigger=CronTrigger(second="*/1"),  # Every 10 seconds
#       id="my_job",  # The `id` assigned to each job MUST be unique
#       max_instances=1,
#       replace_existing=True,
#     )
#     logger.info("Added job 'my_job'.")
#
#     scheduler.add_job(
#       delete_old_job_executions,
#       trigger=CronTrigger(
#         day_of_week="mon", hour="00", minute="00"
#       ),  # Midnight on Monday, before start of the next work week.
#       id="delete_old_job_executions",
#       max_instances=1,
#       replace_existing=True,
#     )
#     logger.info(
#       "Added weekly job: 'delete_old_job_executions'."
#     )
#
#     try:
#       logger.info("Starting scheduler...")
#       scheduler.start()
#     except KeyboardInterrupt:
#       logger.info("Stopping scheduler...")
#       scheduler.shutdown()
#       logger.info("Scheduler shut down successfully!")