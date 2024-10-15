from datetime import datetime, UTC, timedelta

import django.contrib.auth.models
from celery import shared_task
from django.core.mail import send_mail

from .models import Task, User

@shared_task(name="task_manager.end_time_announcer_schedule")
def end_time_announcer_schedule():
	tasks = Task.gather_expiring(datetime.now(UTC) + timedelta(hours=1))
	for i in tasks:
		end_time_announcer.delay(i.id)


@shared_task(name="task_manager.end_time_announcer")
def end_time_announcer(task_id):
	task = Task.find_by_id(task_id)
	user = User.find_by_id(task.user)
	auth = django.contrib.auth.models.User.objects.filter(id=user.id).first()

	mail = send_mail("Task deadline is close",
					 f"{user.name}, your task {task.name} deadline will expire in an hour",
					 "some@email.com",
					 [auth.email])

	return mail
