from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from users.models import User


# Find User and Return User or None if not found
class TrustMeBroAuthentication(BaseAuthentication):
    """Header를 통한 인증
    - Header key값이 없는 경우 -> 로그아웃 처리
    - Hedaer key값으로 User find -> 로그인 시도
    - User 존재하는 경우 -> 로그인 성공
    - User 존재하지 않는 경우(None 반환) -> 로그인 실패
    """

    # BaseAuthentication을 상속 받는 경우 반드시 authenticate 메서드를 재정의(overriding) 해야 함
    # 여기 들어가는 인자인 request는 user가 없는 object임
    # 쿠키도 있고 헤더도 있지만 유저는 없음
    # Header 데이터를 보고 user를 찾는 것은 개발자 몫
    # user를 찾지 못하면 반드시 None을 반환해야 함
    def authenticate(self, request):
        # 쿠키에서 찾는 대신에 secret이라는 헤더에서 찾아보는 것
        # 헤더에 넣어서 보내보는 작업은 Postman에서 header를 직접 만들어 추가해서 API Request를 보내보면 됨
        username = request.headers.get("secret")
        # ✋ 로그아웃 처리
        if not username:
            return None

        # 로그인 시도(username 있음)
        try:
            # ✅ 로그인 성공(DB에서 찾음)
            user = User.objects.get(username=username)
            return (user, None)  # must return tuple (mandatory)
        except User.DoesNotExist:
            # ❌ 로그인 실패(DB에서 찾지 못함)
            raise exceptions.AuthenticationFailed(f"No user {username}")
