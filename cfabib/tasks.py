from __future__ import absolute_import, unicode_literals

from .celerytest import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


# # Create your tasks here
# from __future__ import absolute_import, unicode_literals

# from celery import shared_task
# #from demoapp.models import Widget

# #app = Celery('tasks')#, result_backend = 'postgres://jysmqqojsdlzud:9016579126d99875a49ef7ca8531822114885c7898d388c88a96190d9bb6728c@ec2-174-129-227-205.compute-1.amazonaws.com:5432/deu6vgo7tcseth', broker='amqp://mignwimq:GHhBZBx7Q3C4Wfzic2Vq0M9k6G3aPc3F@spider.rmq.cloudamqp.com/mignwimq')

# #CELERY_BROKER_URL = "amqp://mignwimq:GHhBZBx7Q3C4Wfzic2Vq0M9k6G3aPc3F@spider.rmq.cloudamqp.com/mignwimq"

# @shared_task
# def add(x, y):
#     return x + y
