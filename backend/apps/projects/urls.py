from django.urls import path
from .views import (
    create_project,
    team_project_list,
    project_detail,
    update_project,
    update_project_status,
    delete_project,
)

urlpatterns = [
    path('projects/create/', create_project, name='create_project'),
    path('teams/<int:team_id>/projects/', team_project_list, name='team_project_list'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/<int:project_id>/update/', update_project, name='update_project'),
    path('projects/<int:project_id>/status/', update_project_status, name='update_project_status'),
    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
]