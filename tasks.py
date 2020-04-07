from celery import Celery

app = Celery('tasks',
    broker='amqp://mignwimq:GHhBZBx7Q3C4Wfzic2Vq0M9k6G3aPc3F@spider.rmq.cloudamqp.com/mignwimq',
    backend='db+postgres://jysmqqojsdlzud:9016579126d99875a49ef7ca8531822114885c7898d388c88a96190d9bb6728c@ec2-174-129-227-205.compute-1.amazonaws.com:5432/deu6vgo7tcseth',)

@app.task
def add(x, y):
    return x + y