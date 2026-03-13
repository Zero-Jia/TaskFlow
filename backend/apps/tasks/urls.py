from django.urls import path
from .views import create_task, project_task_list, task_detail

urlpatterns = [
    path('tasks/create/', create_task, name='create_task'),
    path('projects/<int:project_id>/tasks/', project_task_list, name='project_task_list'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
]