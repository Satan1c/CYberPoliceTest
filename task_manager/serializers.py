from datetime import datetime

from rest_framework import serializers

from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['name']


class TaskSerializer(serializers.ModelSerializer):
	@staticmethod
	def parse_tasks(tasks):
		return TaskSerializer(tasks, many=True).data

	@staticmethod
	def parse_task(tasks):
		return TaskSerializer(tasks, many=False).data

	@staticmethod
	def body_to_dict(data):
		result = {}

		var = data.get('name', None)
		result['name'] = str(var) if var is not None and len(str(var).strip()) != 0 else None

		var = data.get('description', None)
		result['description'] = str(var) if var is not None and len(str(var).strip()) != 0 else None

		var = data.get('status', None)
		result['status'] = int(var) if var is not None and int(var) >= 0 else None

		var = data.get('priority', None)
		result['priority'] = int(var) if var is not None and int(var) >= 0 else None

		var = data.get('end_time', None)
		result['end_time'] = datetime.strptime(var, "%Y-%m-%dT%H:%M:%S.%fZ") if var is not None and len(
			str(var).strip()) != 0 else None

		return result

	class Meta:
		model = Task
		fields = ['id', 'name', 'description', 'status', 'priority', 'end_time']
