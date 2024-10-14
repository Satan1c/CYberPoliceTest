from django.conf import settings
from django.contrib.auth import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task, User
from .serializers import TaskSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance: models.User = None, created=False, **kwargs):
	if created:
		User.objects.create(id=instance, name=instance.username).save()


class TaskView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		db = Task.find_by_user_id(request.user.id)
		tasks = TaskSerializer.parse_tasks(db)
		return Response(tasks, status=HTTP_200_OK)

	def post(self, request):
		data = TaskSerializer.body_to_dict(request.data)

		if (name := data.get('name', None)) is None:
			return Response({'error': 'Name is required'}, status=HTTP_400_BAD_REQUEST)

		if (description := data.get('description', None)) is None:
			return Response({'error': 'Description is required'}, status=HTTP_400_BAD_REQUEST)

		if (status := data.get('status', None)) is None:
			return Response({'error': 'Status is required'}, status=HTTP_400_BAD_REQUEST)

		if (priority := data.get('priority', None)) is None:
			return Response({'error': 'Priority is required'}, status=HTTP_400_BAD_REQUEST)

		if (end_time := data.get('end_time', None)) is None:
			return Response({'error': 'End time is required'}, status=HTTP_400_BAD_REQUEST)

		task = Task.create_task(user_id=request.user.id, name=name, description=description, status=status,
								priority=priority, end_time=end_time)

		return Response(TaskSerializer.parse_task(task), status=HTTP_200_OK)


class TargetedTaskView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def put(self, request, task_id):
		if Task.find_by_id(task_id) is None:
			return Response({'error': 'task not found'}, status=HTTP_404_NOT_FOUND)

		data = TaskSerializer.body_to_dict(request.data)

		task = Task.update_task(task_id, data)

		return Response(TaskSerializer.parse_task(task), status=HTTP_200_OK)

	def delete(self, request, task_id):
		if Task.find_by_id(task_id) is None:
			return Response({'error': 'task not found'}, status=HTTP_404_NOT_FOUND)

		Task.delete_task(task_id)

		return Response(str(task_id), status=HTTP_200_OK)
