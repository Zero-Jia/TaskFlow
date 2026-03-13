from django.urls import path
from .views import (
    create_task,
    project_task_list,
    task_detail,
    update_task,
    update_task_status,
    update_task_priority,
    update_task_assignee,
    delete_task,
    project_member_options,
    task_comment_list_create,
    delete_task_comment,
)

urlpatterns = [
    path('tasks/create/', create_task, name='create_task'),
    path('projects/<int:project_id>/tasks/', project_task_list, name='project_task_list'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/status/', update_task_status, name='update_task_status'),
    path('tasks/<int:task_id>/priority/', update_task_priority, name='update_task_priority'),
    path('tasks/<int:task_id>/assignee/', update_task_assignee, name='update_task_assignee'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('projects/<int:project_id>/member-options/', project_member_options, name='project_member_options'),

    path('tasks/<int:task_id>/comments/', task_comment_list_create, name='task_comment_list_create'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/delete/', delete_task_comment, name='delete_task_comment'),
]