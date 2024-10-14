import os

broker_url = os.environ.get('RABBITMQ_URL', os.environ.get("CELERY_BROKER_URL", None))

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

enable_utc = True
