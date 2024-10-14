import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CyberPoliceTest.settings')
app = Celery('CyberPoliceTest')
app.config_from_object('CyberPoliceTest.celeryconfig')
app.autodiscover_tasks()
