from django.urls import path

from .views import TaskView, TargetedTaskView

urlpatterns = [
	path('', TaskView.as_view()),
	path('<task_id>/', TargetedTaskView.as_view()),
]
