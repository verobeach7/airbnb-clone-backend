import strawberry
from strawberry import auto
import typing
from . import models
from users.types import UserType
from reviews.types import ReviewType


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
    # 모든 field의 이름은 Room Model에 있는 이름과 같아야 함
    # 관계를 연결해 줄 때는 ""를 이용하여 적어줘야 함. 당연히 UserType을 임포트해야 함
    owner: "UserType"
    reviews: typing.List["ReviewType"]

    @strawberry.field
    def potato(self) -> str:
        return "lalalla"
