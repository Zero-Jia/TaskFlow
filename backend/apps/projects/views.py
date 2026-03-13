from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.teams.models import Team, TeamMember
from .models import Project
from .serializers import (
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    ProjectStatusUpdateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
)


def check_team_membership(team_id, user):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return None, Response({
            'message': '团队不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    is_member = TeamMember.objects.filter(team=team, user=user).exists()
    if not is_member:
        return None, Response({
            'message': '你不是该团队成员'
        }, status=status.HTTP_403_FORBIDDEN)

    return team, None


def get_project_and_check_membership(project_id, user):
    try:
        project = Project.objects.select_related('team', 'created_by').get(id=project_id)
    except Project.DoesNotExist:
        return None, Response({
            'message': '项目不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    is_member = TeamMember.objects.filter(team=project.team, user=user).exists()
    if not is_member:
        return None, Response({
            'message': '你无权操作该项目'
        }, status=status.HTTP_403_FORBIDDEN)

    return project, None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '创建项目失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    team = serializer.validated_data['team']
    is_member = TeamMember.objects.filter(team=team, user=request.user).exists()
    if not is_member:
        return Response({
            'message': '你不是该团队成员，无法创建项目'
        }, status=status.HTTP_403_FORBIDDEN)

    project = serializer.save(created_by=request.user)

    return Response({
        'message': '项目创建成功',
        'project': ProjectDetailSerializer(project).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_project_list(request, team_id):
    team, error_response = check_team_membership(team_id, request.user)
    if error_response:
        return error_response

    projects = Project.objects.filter(team=team).select_related('team', 'created_by')
    serializer = ProjectListSerializer(projects, many=True)

    return Response({
        'message': '获取项目列表成功',
        'projects': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_detail(request, project_id):
    project, error_response = get_project_and_check_membership(project_id, request.user)
    if error_response:
        return error_response

    serializer = ProjectDetailSerializer(project)
    return Response({
        'message': '获取项目详情成功',
        'project': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_project(request, project_id):
    project, error_response = get_project_and_check_membership(project_id, request.user)
    if error_response:
        return error_response

    serializer = ProjectUpdateSerializer(instance=project, data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '更新项目失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'message': '项目更新成功',
        'project': ProjectDetailSerializer(project).data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_project_status(request, project_id):
    project, error_response = get_project_and_check_membership(project_id, request.user)
    if error_response:
        return error_response

    serializer = ProjectStatusUpdateSerializer(instance=project, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({
            'message': '更新项目状态失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'message': '项目状态更新成功',
        'project': ProjectDetailSerializer(project).data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    project, error_response = get_project_and_check_membership(project_id, request.user)
    if error_response:
        return error_response

    project.delete()

    return Response({
        'message': '项目删除成功'
    }, status=status.HTTP_200_OK)