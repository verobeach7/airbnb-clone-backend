from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.views import APIView

# status 자체를 import하면 status를 타이핑하면 자동완성으로 한번에 볼 수 있음
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from . import serializers
from .models import User


class Me(APIView):
    # 내 모든 정보는 Private이므로 IsAuthenticated 설정
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # Serializer에서 별도의 validation이 필요하지 않음(비밀번호 수정은 다른 url에서 처리)
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        # DRF의 ModelSerializer는 Uniqueness 검증이 이미 포함되어 있음
        # 검증해야 하는 유일한 것은 누군가가 User를 만들 때 password를 설정하는 것만 하면 됨
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        # 사용자가 계정을 생성하기 위해 request를 보내면 그 request에 password가 있는지 검증해야 함
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        try:
            validate_password(password)
        except Exception as e:
            raise ParseError(e)
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # # 아래처럼 하는 것은 password를 암호화하지 않고 그대로 저장하는 것
            # # 절대로 이렇게 해서는 안됨
            # user.password = password

            # User Model의 .set_password() 메서드를 사용
            # .set_password() 메서드는 password를 해쉬화 하여 저장
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
