from django.conf import settings
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
    # reviews: typing.List["ReviewType"]

    ### Pagination
    # 위의 기본 Resolver 대신에 나만의 Resolver 생성
    @strawberry.field
    # self는 rooms, 원하는 인자를 얼마든지 받을 수 있음
    # page 인자를 여기서 요청하면 알아서 전달해 줌
    # Optional 설정을 하면 인자를 받을 수도 받지 않을 수도 있다는 의미
    # `=1`로 하였기 때문에 사용자가 인자를 보내지 않는 경우 page = 1로 설정됨
    def reviews(self, page: typing.Optional[int] = 1) -> typing.List["ReviewType"]:
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    # self에는 rooms가 들어옴
    def rating(self) -> str:
        return self.rating()
