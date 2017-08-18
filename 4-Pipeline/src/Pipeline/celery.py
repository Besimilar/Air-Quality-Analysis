# @author Hongwei
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery('Pipeline',
             broker='amqp://',
             backend='amqp://',
             include=['Pipeline.tasks'])

app.conf.timezone = 'US/Eastern'

app.conf.beat_schedule = {
    # 'run-every-10-minute': {
    #     'task': 'tasks.run',
    #     'schedule': crontab(minute='*/10')
    # }

    'run-every-2-hour': {
        'task': 'tasks.run',
        'schedule': crontab(minute=0, hour='*/2')
    }

    # Executes every Day morning at 8:30 a.m.
    # 'run-every-day-morning': {
    #     'task': 'tasks.run',
    #     # 'schedule': crontab(hour=8, minute=30),
    # },

}

if __name__ == '__main__':
    app.start()
