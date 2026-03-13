from django.urls import path
from .views import create_project,team_project_list,project_detail

urlpatterns = [
    path('projects/create/', create_project, name='create_project'),
    path('teams/<int:team_id>/projects/', team_project_list, name='team_project_list'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
]