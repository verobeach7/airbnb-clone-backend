import strawberry
from strawberry import auto
from . import models


# Strawberry Extension 사용
@strawberry.django.type(models.Room)
class RoomType:
    # Property와 Type을 적어주면 됨
    # name: str
    # strawberry.auto Fuction 사용하면 됨
    # auto는 자동으로 model로 가서 type을 알아내 줌
    id: auto
    name: auto
    kind: auto
