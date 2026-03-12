from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    AvatarUploadSerializer,
)


@api_view(['GET'])
def health_check(request):
    return Response({
        'message': 'TaskFlow backend is running',
        'status': 'ok'
    })


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': '注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        'message': '注册失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'message': '登录成功',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'message': '登录失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response({
        'message': '获取当前用户信息成功',
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        profile_serializer = UserProfileSerializer(user, context={'request': request})
        return Response({
            'message': '个人信息更新成功',
            'user': profile_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'message': '个人信息更新失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({
                'message': '修改密码失败',
                'errors': {
                    'old_password': ['旧密码错误']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({
            'message': '密码修改成功，请重新登录'
        }, status=status.HTTP_200_OK)

    return Response({
        'message': '修改密码失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    serializer = AvatarUploadSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        profile_serializer = UserProfileSerializer(user, context={'request': request})
        return Response({
            'message': '头像上传成功',
            'user': profile_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'message': '头像上传失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)