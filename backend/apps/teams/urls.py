from django.urls import path
from .views import (
    create_team,
    team_list,
    team_detail,
    team_members,
    invite_team_member,
    update_team_member_role,
    remove_team_member,
)

urlpatterns = [
    path('teams/', team_list, name='team_list'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/<int:team_id>/', team_detail, name='team_detail'),
    path('teams/<int:team_id>/members/', team_members, name='team_members'),
    path('teams/<int:team_id>/invite/', invite_team_member, name='invite_team_member'),
    path('teams/<int:team_id>/members/<int:member_id>/role/', update_team_member_role, name='update_team_member_role'),
    path('teams/<int:team_id>/members/<int:member_id>/remove/', remove_team_member, name='remove_team_member'),
]