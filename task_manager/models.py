import uuid
from datetime import datetime

import django.contrib.auth.models
from django.db import models


class User(models.Model):
	id = models.OneToOneField(django.contrib.auth.models.User, unique=True, primary_key=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)

	class Meta:
		db_table = 'users'
		verbose_name = 'User'
		verbose_name_plural = 'Users'
		indexes = [models.Index(fields=['name'])]
		ordering = ['name']

	def __str__(self):
		return self.name

	@classmethod
	def find_by_id(cls, user_id: int):
		return cls.objects.filter(id=user_id).first()

	@classmethod
	def create_user(cls, user: django.contrib.auth.models.User):
		cls.objects.create(id=user, name=user.get_username()).save()


# class Status(enum.Enum):
# class Priority(enum.Enum):

class Task(models.Model):
	id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	name = models.CharField(max_length=100)
	description = models.TextField(max_length=500)

	status = models.IntegerField(default=0)
	priority = models.IntegerField(default=0)

	end_time = models.DateTimeField(null=True, )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'tasks'
		verbose_name = 'Task'
		verbose_name_plural = 'Tasks'
		indexes = [
			models.Index(fields=['user_id']),
			models.Index(fields=['name']),
			models.Index(fields=['status']),
			models.Index(fields=['priority']),
			models.Index(fields=['end_time']),
		]
		ordering = ['name', 'end_time', 'created_at', 'updated_at']

	def __str__(self):
		return self.name

	@classmethod
	def find_by_id(cls, task_id: int):
		res = list(cls.objects.filter(id=task_id))
		return res.pop() if len(res) > 0 else None

	@classmethod
	def find_by_user_id(cls, user_id: int):
		return list(cls.objects.filter(user_id=user_id))

	@classmethod
	def delete_task(cls, task_id: int):
		return cls.objects.filter(id=task_id).first().delete()

	@classmethod
	def update_task(cls, task_id: int, data: dict):
		task = cls.find_by_id(task_id)

		if (name := data.get("name", None)) is not None:
			task.name = name

		if (description := data.get("description", None)) is not None:
			task.description = description

		if (status := data.get("status", None)) is not None:
			task.status = status

		if (priority := data.get("priority", None)) is not None:
			task.priority = priority

		if (end_time := data.get("end_time", None)) is not None:
			task.end_time = end_time

		task.save()

		return task

	@classmethod
	def create_task(cls, user_id: int, name: str, description: str, status: int, priority: int, end_time: datetime):
		task = cls.objects.create(user=User.find_by_id(user_id), name=name, description=description, status=status,
								  priority=priority, end_time=end_time)
		task.save()

		return task
