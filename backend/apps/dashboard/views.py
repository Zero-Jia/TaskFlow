from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.tasks.models import Task


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    # 当前用户被分配的任务
    assigned_tasks = Task.objects.filter(assignee=user)

    # 当前用户创建的任务
    created_tasks = Task.objects.filter(creator=user)

    # 基础统计
    total_assigned = assigned_tasks.count()
    total_created = created_tasks.count()

    # 状态统计
    status_counts = {
        'todo': assigned_tasks.filter(status='todo').count(),
        'in_progress': assigned_tasks.filter(status='in_progress').count(),
        'done': assigned_tasks.filter(status='done').count(),
        'overdue': assigned_tasks.filter(status='overdue').count(),
    }

    # 优先级统计
    priority_counts = {
        'low': assigned_tasks.filter(priority='low').count(),
        'medium': assigned_tasks.filter(priority='medium').count(),
        'high': assigned_tasks.filter(priority='high').count(),
        'urgent': assigned_tasks.filter(priority='urgent').count(),
    }

    # 衍生统计：未完成任务数
    unfinished_count = assigned_tasks.filter(
        Q(status='todo') | Q(status='in_progress') | Q(status='overdue')
    ).count()

    # 衍生统计：高优先级任务数
    high_priority_count = assigned_tasks.filter(
        Q(priority='high') | Q(priority='urgent')
    ).count()

    return Response({
        'message': '获取统计数据成功',
        'stats': {
            'total_assigned_tasks': total_assigned,
            'total_created_tasks': total_created,
            'unfinished_tasks': unfinished_count,
            'high_priority_tasks': high_priority_count,
            'status_counts': status_counts,
            'priority_counts': priority_counts,
        }
    }, status=status.HTTP_200_OK)