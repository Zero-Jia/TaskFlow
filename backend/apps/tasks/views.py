from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

from apps.projects.models import Project
from apps.teams.models import TeamMember
from apps.notifications.models import Notification
from .models import Task, Comment
from .serializers import (
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskStatusUpdateSerializer,
    TaskPriorityUpdateSerializer,
    TaskAssigneeUpdateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    CommentSerializer,
    ProjectMemberOptionSerializer,
    TaskBoardCardSerializer,
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

    # 创建任务时，如果指定了负责人，并且负责人不是当前创建人，则创建通知
    if task.assignee and task.assignee != request.user:
        Notification.objects.create(
            user=task.assignee,
            type='task_assigned',
            content=f'你被指派为任务《{task.title}》的负责人',
            related_task_id=task.id
        )

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

    tasks = Task.objects.filter(project=project).select_related(
        'project', 'creator', 'assignee'
    )

    # 获取查询参数
    search_param = request.query_params.get('search')
    status_param = request.query_params.get('status')
    priority_param = request.query_params.get('priority')
    assignee_param = request.query_params.get('assignee')
    ordering_param = request.query_params.get('ordering')
    page_param = request.query_params.get('page', 1)

    # 搜索：按标题模糊搜索
    if search_param:
        tasks = tasks.filter(title__icontains=search_param)

    # 状态筛选
    if status_param:
        tasks = tasks.filter(status=status_param)

    # 优先级筛选
    if priority_param:
        tasks = tasks.filter(priority=priority_param)

    # 负责人筛选
    if assignee_param:
        if assignee_param == 'unassigned':
            tasks = tasks.filter(assignee__isnull=True)
        else:
            tasks = tasks.filter(assignee_id=assignee_param)

    # 排序
    allowed_ordering = ['due_date', '-due_date', 'created_at', '-created_at']
    if ordering_param in allowed_ordering:
        tasks = tasks.order_by(ordering_param)
    else:
        tasks = tasks.order_by('-created_at')

    # 分页：每页固定 5 条
    paginator = Paginator(tasks, 5)

    try:
        page_obj = paginator.page(page_param)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    serializer = TaskListSerializer(page_obj.object_list, many=True)

    return Response({
        'message': '获取任务列表成功',
        'tasks': serializer.data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    serializer = TaskUpdateSerializer(instance=task, data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '更新任务失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'message': '任务更新成功',
        'task': TaskDetailSerializer(task).data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    serializer = TaskStatusUpdateSerializer(instance=task, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({
            'message': '更新任务状态失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'message': '任务状态更新成功',
        'task': TaskDetailSerializer(task).data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_priority(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    serializer = TaskPriorityUpdateSerializer(instance=task, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({
            'message': '更新任务优先级失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'message': '任务优先级更新成功',
        'task': TaskDetailSerializer(task).data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_assignee(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    old_assignee = task.assignee

    serializer = TaskAssigneeUpdateSerializer(instance=task, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({
            'message': '更新任务负责人失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    task.refresh_from_db()

    # 只有在负责人真的发生变化时，才发送通知
    if task.assignee and task.assignee != old_assignee and task.assignee != request.user:
        Notification.objects.create(
            user=task.assignee,
            type='task_assigned',
            content=f'你被指派为任务《{task.title}》的负责人',
            related_task_id=task.id
        )

    return Response({
        'message': '任务负责人更新成功',
        'task': TaskDetailSerializer(task).data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    task.delete()

    return Response({
        'message': '任务删除成功'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_member_options(request, project_id):
    project, error_response = check_project_membership(project_id, request.user)
    if error_response:
        return error_response

    members = TeamMember.objects.filter(team=project.team).select_related('user').order_by('joined_at')
    serializer = ProjectMemberOptionSerializer(members, many=True)

    return Response({
        'message': '获取项目成员选项成功',
        'members': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_comment_list_create(request, task_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    if request.method == 'GET':
        comments = Comment.objects.filter(task=task).select_related('author').order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'message': '获取评论列表成功',
            'comments': serializer.data
        }, status=status.HTTP_200_OK)

    content = request.data.get('content', '').strip()
    if not content:
        return Response({
            'message': '发表评论失败',
            'errors': {
                'content': ['评论内容不能为空']
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(
        task=task,
        author=request.user,
        content=content
    )

    # 给负责人发通知
    if task.assignee and task.assignee != request.user:
        Notification.objects.create(
            user=task.assignee,
            type='task_comment',
            content=f'任务《{task.title}》有新评论',
            related_task_id=task.id
        )

    # 给任务创建者发通知，避免重复通知
    if task.creator != request.user and task.creator != task.assignee:
        Notification.objects.create(
            user=task.creator,
            type='task_comment',
            content=f'任务《{task.title}》有新评论',
            related_task_id=task.id
        )

    return Response({
        'message': '评论发布成功',
        'comment': CommentSerializer(comment).data
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task_comment(request, task_id, comment_id):
    task, error_response = get_task_and_check_membership(task_id, request.user)
    if error_response:
        return error_response

    try:
        comment = Comment.objects.select_related('author', 'task').get(id=comment_id, task=task)
    except Comment.DoesNotExist:
        return Response({
            'message': '评论不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    if comment.author != request.user:
        return Response({
            'message': '你只能删除自己的评论'
        }, status=status.HTTP_403_FORBIDDEN)

    comment.delete()

    return Response({
        'message': '评论删除成功'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_task_board(request, project_id):
    project, error_response = check_project_membership(project_id, request.user)
    if error_response:
        return error_response

    tasks = Task.objects.filter(project=project).select_related('assignee')

    todo_tasks = tasks.filter(status='todo').order_by('due_date', '-created_at')
    in_progress_tasks = tasks.filter(status='in_progress').order_by('due_date', '-created_at')
    done_tasks = tasks.filter(status='done').order_by('due_date', '-created_at')
    overdue_tasks = tasks.filter(status='overdue').order_by('due_date', '-created_at')

    return Response({
        'message': '获取任务看板成功',
        'board': {
            'todo': TaskBoardCardSerializer(todo_tasks, many=True).data,
            'in_progress': TaskBoardCardSerializer(in_progress_tasks, many=True).data,
            'done': TaskBoardCardSerializer(done_tasks, many=True).data,
            'overdue': TaskBoardCardSerializer(overdue_tasks, many=True).data,
        }
    }, status=status.HTTP_200_OK)