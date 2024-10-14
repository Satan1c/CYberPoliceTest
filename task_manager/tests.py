import django.contrib.auth.models
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from task_manager import models
from .views import TaskView, TargetedTaskView


class TaskViewsTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		if django.contrib.auth.models.User.objects.count() < 1:
			auth = django.contrib.auth.models.User.objects.create_superuser('satan1c', None, '1')

			if models.User.objects.count() < 1:
				user = models.User.create_user(auth)

	def test_get_returns_empty_list(self):
		class Request:
			def __init__(self):
				self.user = django.contrib.auth.models.User.objects.first()

		result = TaskView.get(None, Request())

		target_result = Response([], status=HTTP_200_OK)
		self.assertEqual(result.data, target_result.data)
		self.assertEqual(result.status_code, target_result.status_code)

	def test_post_returns_valid_object(self):
		class Request:
			def __init__(self):
				self.user = django.contrib.auth.models.User.objects.first()
				self.data = {
					'name': 'Test task',
					'description': 'some description',
					'status': 1,
					'priority': 2,
					'end_time': '2026-04-13T13:06:07.000007Z',
				}

		request = Request()
		result = TaskView.post(None, request)

		self.assertEqual(result.status_code, HTTP_200_OK)
		self.assertIsNotNone(result.data.get('id', None))
		self.assertEqual(result.data.get('name', None), request.data['name'])
		self.assertEqual(result.data.get('description', None), request.data['description'])
		self.assertEqual(result.data.get('status', None), request.data['status'])
		self.assertEqual(result.data.get('priority', None), request.data['priority'])
		self.assertEqual(str(result.data.get('end_time', None)), request.data['end_time'])

	def test_put_returns_updated_object(self):
		class Request:
			def __init__(self, data: dict):
				self.user = django.contrib.auth.models.User.objects.first()
				self.data = data

		request = Request({
			'name': 'Test task',
			'description': 'some description',
			'status': 1,
			'priority': 2,
			'end_time': '2026-04-13T13:06:07.000007Z',
		})

		TaskView.post(None, request)
		task = models.Task.objects.first()

		request = Request({
			'name': 'New task',
			'description': 'another description',
			'status': 2,
			'priority': 1,
			'end_time': '2026-05-13T13:06:07.000007Z',
		})

		updated = TargetedTaskView.put(None, request, task.id)

		self.assertEqual(updated.status_code, HTTP_200_OK)

		self.assertEqual(updated.data.get('name', None), request.data['name'])
		self.assertNotEqual(updated.data.get('name', None), task.name)

		self.assertEqual(updated.data.get('description', None), request.data['description'])
		self.assertNotEqual(updated.data.get('description', None), task.description)

		self.assertEqual(updated.data.get('status', None), request.data['status'])
		self.assertNotEqual(updated.data.get('status', None), task.status)

		self.assertEqual(updated.data.get('priority', None), request.data['priority'])
		self.assertNotEqual(updated.data.get('priority', None), task.priority)

		self.assertEqual(str(updated.data.get('end_time', None)), request.data['end_time'])
		self.assertNotEqual(updated.data.get('end_time', None), task.end_time)

	def test_delete_returns_updated_object(self):
		class Request:
			def __init__(self, data: dict):
				self.user = django.contrib.auth.models.User.objects.first()
				self.data = data

		request = Request({
			'name': 'Test task',
			'description': 'some description',
			'status': 1,
			'priority': 2,
			'end_time': '2026-04-13T13:06:07.000007Z',
		})

		TaskView.post(None, request)
		task = models.Task.objects.first()

		deleted = TargetedTaskView.delete(None, None, task.id)

		self.assertEqual(deleted.status_code, HTTP_200_OK)
		self.assertEqual(str(deleted.data), str(task.id))
