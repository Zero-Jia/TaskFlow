from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegisterSerializer


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