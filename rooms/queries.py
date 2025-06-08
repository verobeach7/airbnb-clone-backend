from . import models


# 함수 이름은 원하는 이름으로 지으면 됨
def get_all_rooms():
    # Django REST Framework와 달리 serialization이 필요하지 않음
    # Strawberry가 알아서 필요한 type list로 변환해 줌
    return models.Room.objects.all()
