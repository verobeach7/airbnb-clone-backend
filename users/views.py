# authenticate: username과 password를 돌려주는 function - 인증에 성공하면 User를 반환
# login: User를 로그인시켜주는 function - User와 함께 Request를 보내면 브라우저가 필요로 하는 cookies와 token 등 중요한 데이터를 자동으로 생성해 줌
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password

# settings.py에 직접 접근할 수 있음. 여기에 설정해 놓은 환경변수를 바로 가져와 사용 가능
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

# status 자체를 import하면 status를 타이핑하면 자동완성으로 한번에 볼 수 있음
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
import jwt
import requests
from . import serializers
from .models import User
from rooms.models import Room
from bookings.models import Booking
from rooms import serializers as RoomSerializer
from bookings import serializers as BookingSerializer
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


class userBookedRooms(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_booked_list = Booking.objects.filter(
            user=request.user,
            kind=Booking.BookingKindChoices.ROOM,
        )
        # print(all_booked_list)  # QuerySet을 받음
        # QuerySet이나 Model Instance를 JSON으로 응답하기 위해 serializer 사용
        # 데이터 검증, 직렬화, 역직렬화를 위해 사용됨
        serializer = BookingSerializer.UserBookedRoomSerializer(
            all_booked_list,
            many=True,  # all_booked_list가 여러 개를 담고 있는 Array이기 때문에 설정
        )
        # print(serializer.data)
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
            return Response(
                {"ok": "welcome!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
        try:

            # Frontend로부터 받아온 깃허브 OAuth 코드
            code = request.data.get("code")
            # 이 코드를 가지고 Github에서 Access Token으로 교환해야 함
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=Ov23liRvQnZqj0Iril2U&client_secret={settings.GH_SECRET}",
                # json으로 보내달라고 요청
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            # access token을 가지고 Github API와 소통할 수 있음
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            """
            {'message': 'Bad credentials', 'documentation_url': 'https://docs.github.com/rest', 'status': '401'}
            [25/Jun/2025 19:37:31] "POST /api/v1/users/github HTTP/1.1" 200 0
            [{'email': 'verobeach7@gmail.com', 'primary': True, 'verified': True, 'visibility': 'private'}, {'email': '60215757+verobeach7@users.noreply.github.com', 'primary': False, 'verified': True, 'visibility': None}]
            [25/Jun/2025 19:37:31] "POST /api/v1/users/github HTTP/1.1" 200 0
            """
            # Bad credentials: Frontend가 Development Mode에서 Strict Mode로 작동하고 있어서 발생하는 현상
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login") + "_gh:" + str(user_data.get("id")),
                    email=user_emails[0]["email"],
                    name=user_data.get("name") if user_data.get("name") else "",
                    avatar=user_data.get("avatar_url"),
                )
                # set_unusable_password() 설정을 통해 Social Login을 한 사람인지 아닌지 판단하기 가장 좋은 방법 중 하나임
                user.set_unusable_password()
                user.save()
                # login()함수를 호출하면 장고가 알아서 백엔드에 세션을 만들어 주고 유저에게 쿠키를 주는 등 모든 것을 다 자동으로 해줌
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            # print(code)
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "a4e1b24eef7b898ce0cb1c33edfa353f",
                    "redirect_uri": "http://127.0.0.1:5173/social/kakao",
                    "code": code,
                },
            )
            # print(access_token.json())
            # {'access_token': 'YWLs6iizhdeW......', 'token_type': 'bearer', 'refresh_token': 'vGDxT8bHNMQh-a0uh69v--......', 'expires_in': 21599, 'scope': 'account_email profile_image profile_nickname', 'refresh_token_expires_in': 5183999}
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer ${access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            # print(user_data)
            # {'id': 432200......, 'connected_at': '2025-06-26T04:27:14Z', 'properties': {'nickname': '희성', 'profile_image': 'http://k.kakaocdn.net/dn/c88j6T/btsJQ2sjOzH/RiraK....../img_640x640.jpg', 'thumbnail_image': 'http://k.kakaocdn.net/dn/c88j6T/btsJQ2sjOzH/Ri...../img_110x110.jpg'}, 'kakao_account': {'profile_nickname_needs_agreement': False, 'profile_image_needs_agreement': False, 'profile': {'nickname': '희성', 'thumbnail_image_url': 'http://k.kakaocdn.net/dn/c88j6T/btsJQ2sjOzH/Rira.......jpg', 'profile_image_url': 'http://k.kakaocdn.net/dn/c88j6T/btsJQ2sjOzH/RiraKv....../img_640x640.jpg', 'is_default_image': False, 'is_default_nickname': False}, 'has_email': True, 'email_needs_agreement': False, 'is_email_valid': True, 'is_email_verified': True, 'email': 'verobe......'}}
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            name = request.data.get("name")
            email = request.data.get("email")

            print(username, password, name, email)

            # 프론트엔드에서 username, password, name, email이 제대로 넘어왔는지에 대한 검증 필요. 사용자를 신뢰하지 말기
            if email == "" or username == "" or name == "" or password == "":
                return Response(
                    {
                        "fail": "Required field is missing",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 이름과 비밀번호는 다른 사용자와 같을 수 있음
            # username이나 email이 같은 사용자가 존재하는 경우 이것을 이용하여 가입 불가
            if User.objects.filter(username=username):
                return Response(
                    {
                        "fail": "This username is already taken",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(email=email):
                return Response(
                    {"fail": "This email is already taken"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(
                username=username,
                name=name,
                email=email,
            )
            user.set_password(password)
            user.save()
            login(request, user)

            return Response(
                {
                    "success": "Created the user",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Occurred some error while signing up as {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
