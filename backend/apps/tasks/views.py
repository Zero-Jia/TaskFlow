from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.projects.models import Project
from apps.teams.models import TeamMember
from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
)


def check_project_membership(project_id, user):
    try:
        project = Project.objects.select_related('team').get(id=project_id)
    except Project.DoesNotExist:
        return None, Response({
            'message': '项目不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    is_member = TeamMember.objects.filter(team=project.team, user=user).exists()
    if not is_member:
        return None, Response({
            'message': '你不是该项目所属团队成员'
        }, status=status.HTTP_403_FORBIDDEN)

    return project, None


def get_task_and_check_membership(task_id, user):
    try:
        task = Task.objects.select_related('project__team', 'creator', 'assignee').get(id=task_id)
    except Task.DoesNotExist:
        return None, Response({
            'message': '任务不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    is_member = TeamMember.objects.filter(team=task.project.team, user=user).exists()
    if not is_member:
        return None, Response({
            'message': '你无权查看该任务'
        }, status=status.HTTP_403_FORBIDDEN)

    return task, None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '创建任务失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    project = serializer.validated_data['project']
    is_member = TeamMember.objects.filter(team=project.team, user=request.user).exists()
    if not is_member:
        return Response({
            'message': '你不是该项目所属团队成员，无法创建任务'
        }, status=status.HTTP_403_FORBIDDEN)

    task = serializer.save(creator=request.user)

    return Response({
        'message': '任务创建成功',
        'task': TaskDetailSerializer(task).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_task_list(request, project_id):
    project, error_response = check_project_membership(project_id, request.user)
    if error_response:
        return error_response

    tasks = Task.objects.filter(project=project).select_related('project', 'creator', 'assignee')
    serializer = TaskListSerializer(tasks, many=True)

    return Response({
        'message': '获取任务列表成功',
        'tasks': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    serializer = TaskDetailSerializer(task)
    return Response({
        'message': '获取任务详情成功',
        'task': serializer.data
    }, status=status.HTTP_200_OK)