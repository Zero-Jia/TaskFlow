from django.contrib.auth import get_user_model
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
    TeamInviteSerializer,
    TeamRoleUpdateSerializer,
    TeamMemberSerializer,
)

User = get_user_model()


def get_team_and_membership(team_id, user):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return None, None, Response({
            'message': '团队不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        membership = TeamMember.objects.get(team=team, user=user)
    except TeamMember.DoesNotExist:
        return team, None, Response({
            'message': '你不是该团队成员'
        }, status=status.HTTP_403_FORBIDDEN)

    return team, membership, None


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
    teams = Team.objects.filter(members__user=request.user).distinct().order_by('-created_at')
    serializer = TeamListSerializer(teams, many=True)
    return Response({
        'message': '获取团队列表成功',
        'teams': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_detail(request, team_id):
    team, membership, error_response = get_team_and_membership(team_id, request.user)
    if error_response:
        return error_response

    serializer = TeamDetailSerializer(team)
    return Response({
        'message': '获取团队详情成功',
        'team': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_members(request, team_id):
    team, membership, error_response = get_team_and_membership(team_id, request.user)
    if error_response:
        return error_response

    members = TeamMember.objects.filter(team=team).select_related('user').order_by('joined_at')
    serializer = TeamMemberSerializer(members, many=True)

    return Response({
        'message': '获取团队成员成功',
        'members': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_team_member(request, team_id):
    team, membership, error_response = get_team_and_membership(team_id, request.user)
    if error_response:
        return error_response

    if membership.role != 'owner':
        return Response({
            'message': '只有团队拥有者可以邀请成员'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = TeamInviteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '邀请成员失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']

    try:
        user_to_invite = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            'message': '该用户不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    if TeamMember.objects.filter(team=team, user=user_to_invite).exists():
        return Response({
            'message': '该用户已在团队中'
        }, status=status.HTTP_400_BAD_REQUEST)

    new_member = TeamMember.objects.create(
        team=team,
        user=user_to_invite,
        role='member'
    )

    return Response({
        'message': '邀请成员成功',
        'member': TeamMemberSerializer(new_member).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_team_member_role(request, team_id, member_id):
    team, membership, error_response = get_team_and_membership(team_id, request.user)
    if error_response:
        return error_response

    if membership.role != 'owner':
        return Response({
            'message': '只有团队拥有者可以修改成员角色'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        target_member = TeamMember.objects.select_related('user').get(id=member_id, team=team)
    except TeamMember.DoesNotExist:
        return Response({
            'message': '团队成员不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    if target_member.role == 'owner':
        return Response({
            'message': '不能修改拥有者角色'
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = TeamRoleUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '修改角色失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    target_member.role = serializer.validated_data['role']
    target_member.save()

    return Response({
        'message': '成员角色修改成功',
        'member': TeamMemberSerializer(target_member).data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_team_member(request, team_id, member_id):
    team, membership, error_response = get_team_and_membership(team_id, request.user)
    if error_response:
        return error_response

    if membership.role != 'owner':
        return Response({
            'message': '只有团队拥有者可以移除成员'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        target_member = TeamMember.objects.select_related('user').get(id=member_id, team=team)
    except TeamMember.DoesNotExist:
        return Response({
            'message': '团队成员不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    if target_member.role == 'owner':
        return Response({
            'message': '不能移除团队拥有者'
        }, status=status.HTTP_400_BAD_REQUEST)

    target_member.delete()

    return Response({
        'message': '成员移除成功'
    }, status=status.HTTP_200_OK)