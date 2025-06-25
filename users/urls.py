from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    # 이 위치에 있으면 장고는 urlpatterns를 위에서부터 차례대로 확인하기 때문에 /users/me로 이동 시 에러가 발생함: me를 <str:username>으로 받아들임
    # path("<str:username>", views.PublicUser.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    ### 방법1. username과 password를 이용한 쿠키 로그인
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    ### 방법2. Token Authentication
    # 토큰을 얻을 수 있는 API URL 생성
    # obtain_auth_token을 DRF에서 사전에 만들어 놓은 API View
    # ID, PASSWORD가 인증되면 토큰을 보내주도록 제작되어 있음
    path("token-login", obtain_auth_token),
    ### 방법3. JWT Authentication
    path("jwt-login", views.JWTLogIn.as_view()),
    path("github", views.GithubLogIn.as_view()),
    # 이 위치에 놓으면 정상 작동
    # path("<str:username>", views.PublicUser.as_view()),
    # 하지만 username이 me인 사용자가 실제로 존재한다면?
    path("@<str:username>", views.PublicUser.as_view()),
    # @를 사용함으로써 `users/me`와 `users/@me`로 구분하여 사용
    # `users/me`는 사용자 본인의 프로필을 보게 되고, `users/@me`는 me라는 username을 가진 사용자의 프로필을 보게 됨
    path("@<str:username>/rooms", views.UserRooms.as_view()),
    path("@<str:username>/reviews", views.UserReviews.as_view()),
]
