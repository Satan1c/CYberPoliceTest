import os

from celery.schedules import crontab

broker_url = os.environ.get('RABBITMQ_URL', os.environ.get("CELERY_BROKER_URL", None))

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

beat_schedule = {
	'end_time-announcer-schedule': {
		'task': 'task_manager.end_time_announcer_schedule',
		'schedule': crontab(minute='*/20')
	},
}

timezone = 'UTC'
enable_utc = True
