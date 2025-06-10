from . import models

# schema.py 파일에서 인증 시 여기서는 Info를 import할 필요 없음
# from strawberry.types import Info


# 함수 이름은 원하는 이름으로 지으면 됨
def get_all_rooms():
    # Django REST Framework와 달리 serialization이 필요하지 않음
    # Strawberry가 알아서 필요한 type list로 변환해 줌

    # if info.context.request.user.is_authenticated:
    #     return models.Room.objects.all()
    # else:
    #     raise Exception("Not auth.")
    # if-else문을 이용하여 그닥 섹시하지 않음

    # views.py의 permission_classes와 같은 역할을 하는 것이 Strawberry에도 있음
    # 여기서 설정하지 않고 get_all_rooms를 호출하는 schema.py 파일에서 설정하면 됨
    # 이 방식 사용 시 get_all_rooms의 parameter로 `info: Info`를 넣어주지 않아도 됨
    # 모든 것은 schema.py에서 설정하면 됨
    return models.Room.objects.all()


def get_room(pk: int):
    try:
        return models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        return None
