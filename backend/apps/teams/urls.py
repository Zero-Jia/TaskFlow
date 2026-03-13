from django.urls import path
from .views import create_team, team_list, team_detail

urlpatterns = [
    path('teams/', team_list, name='team_list'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/<int:team_id>/', team_detail, name='team_detail'),
]