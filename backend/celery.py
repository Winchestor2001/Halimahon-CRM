import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

hours = 2

app.conf.beat_schedule = {
    f'check-rooms-{hours}-minute': {
        'task': 'api.tasks.check_patient_rooms',
        'schedule': crontab(hour=f'*/{hours}'),
    }

}
