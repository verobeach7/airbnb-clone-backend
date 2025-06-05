from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    # 이 위치에 있으면 장고는 urlpatterns를 위에서부터 차례대로 확인하기 때문에 /users/me로 이동 시 에러가 발생함: me를 <str:username>으로 받아들임
    # path("<str:username>", views.PublicUser.as_view()),
    path("me", views.Me.as_view()),
    # 이 위치에 놓으면 정상 작동
    # path("<str:username>", views.PublicUser.as_view()),
    # 하지만 username이 me인 사용자가 실제로 존재한다면?
    path("@<str:username>", views.PublicUser.as_view()),
    # @를 사용함으로써 `users/me`와 `users/@me`로 구분하여 사용
    # `users/me`는 사용자 본인의 프로필을 보게 되고, `users/@me`는 me라는 username을 가진 사용자의 프로필을 보게 됨
]
