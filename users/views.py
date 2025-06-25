# authenticate: username과 password를 돌려주는 function - 인증에 성공하면 User를 반환
# login: User를 로그인시켜주는 function - User와 함께 Request를 보내면 브라우저가 필요로 하는 cookies와 token 등 중요한 데이터를 자동으로 생성해 줌
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

# status 자체를 import하면 status를 타이핑하면 자동완성으로 한번에 볼 수 있음
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
import jwt
from . import serializers
from .models import User
from rooms.models import Room
from rooms import serializers as RoomSerializer
from reviews.models import Review
from reviews import serializers as ReviewSerializer


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
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class UserRooms(APIView):
    def get(self, request, username):
        all_rooms = Room.objects.filter(owner__username=username)
        serializer = RoomSerializer.RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data)


class UserReviews(APIView):
    def get(self, request, username):
        all_reviews = Review.objects.filter(user__username=username)
        serializer = ReviewSerializer.ReviewSerializer(
            all_reviews,
            many=True,
        )
        return Response(serializer.data)


class ChangePassword(APIView):
    # 인증되지 않은 사용자는 호출할 수 없도록 막아야 함
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        # old_password나 new_password가 없으면 에러를 발생시켜야 함
        if not old_password or not new_password:
            raise ParseError
        # 장고는 old_password가 현재 비밀번호가 맞는지 확인해주는 utility를 가지고 있음
        # .check_password() 메서드 사용
        if user.check_password(old_password):
            # set_password는 new_password를 hash할 때만 작동
            user.set_password(new_password)
            # 저장하지 않으면 hash만 되고 새로운 비밀번호로 설정되지 않음
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # authenticate() 함수는 User를 반환할 수도 있고 안 할 수도 있음
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # request와 user를 담아 login() 함수를 호출하면 장고가 알아서 로그인 시킴
            login(request, user)
            return Response({"ok": "welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    # LogOut을 하기 위해서는 LogIn되어 있어야 하므로 자격 증명을 확인해야 함
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request와 함께 logout() 함수만 호출하면 됨
        logout(request)
        return Response({"ok": "bye!"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # authenticate() 함수는 User를 반환할 수도 있고 안 할 수도 있음
        # username과 password가 올바르면 User 반환
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # 토큰 생성 후 User에게 전달. 유저가 원하면 토큰을 복호화 할 수 있기 때문에 민감한 정보를 토큰에 담아서는 안 됨!!!
            # JWT 토큰이 암호화 되는 것은 아님. 대신 우리가 준 토큰인지 수정되었는지를 알 수 있음.
            # JWT 토큰 안에 넣는 정보는 공개적인 것이어야 함
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):
    def post(self, request):
        code = request.data.get("code")
        print(code)
        return Response()
