# permissions는 여기 저기서 사용할 것이기 때문에 common에 별도 파일로 생성

import typing
from strawberry.permission import BasePermission
from strawberry.types import Info


# 원하는 Permission을 생성하여 사용
# Query의 permission_classes 리스트에 넣어주기만 하면 됨
# queries.py 파일에 인증을 위한 어떤 로직도 작성할 필요 없이 schema.py에서 권한을 만들어 부여만 해주면 됨
class OnlyLoggedIn(BasePermission):
    # 여기 만든 Permission에 의해 User를 차단했을 경우 보여야 하는 에러 메시지를 설정할 수 있음
    message = "You need to be logged in for this!"

    # # has_permission 타이핑 후 엔터만 눌러주면 자동완성 됨
    # def has_permission(self, source, info, **kwargs):
    #     return super().has_permission(source, info, **kwargs)

    # source와 info만 사용하면 됨. 나머지는 삭제해도 됨.
    # source에 Any, info에 Info 타입 설정을 해야 함
    def has_permission(self, source: typing.Any, info: Info):
        # 테스트를 위해 모든 사용자 차단
        # return False  # 실제로 로그인 되어 있어도 여기서 False를 반환했기 때문에 로그인 해야 한다는 에러 메시지를 확인할 수 있음

        # if info.context.request.user.is_authenticated:
        #     return True
        # else:
        #     return False

        # is_authenticated는 True or False를 반환하기 때문에 바로 반환해도 됨
        return info.context.request.user.is_authenticated
