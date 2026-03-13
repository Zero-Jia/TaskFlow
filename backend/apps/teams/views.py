from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Team, TeamMember
from .serializers import (
    TeamCreateSerializer,
    TeamListSerializer,
    TeamDetailSerializer,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    serializer = TeamCreateSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            team = serializer.save(owner=request.user)

            TeamMember.objects.create(
                team=team,
                user=request.user,
                role='owner'
            )

        return Response({
            'message': '团队创建成功',
            'team': TeamDetailSerializer(team).data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'message': '团队创建失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_list(request):
    teams = Team.objects.filter(
        members__user=request.user
    ).distinct().order_by('-created_at')

    serializer = TeamListSerializer(teams, many=True)
    return Response({
        'message': '获取团队列表成功',
        'teams': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_detail(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({
            'message': '团队不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    is_member = TeamMember.objects.filter(team=team, user=request.user).exists()
    if not is_member:
        return Response({
            'message': '无权查看该团队'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = TeamDetailSerializer(team)
    return Response({
        'message': '获取团队详情成功',
        'team': serializer.data
    }, status=status.HTTP_200_OK)