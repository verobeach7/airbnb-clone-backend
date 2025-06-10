from django.conf import settings
import strawberry

# strawberry.types
# Info: 강력한 Info Parameter Type을 사용할 수 있게 됨
from strawberry.types import Info
from strawberry import auto
import typing
from . import models
from wishlists.models import Wishlist
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

    @strawberry.field
    # (parameter) self: Self@RoomType - self는 room을 받음
    # Info parameter는 현재 발생하는 request에 대한 많은 정보를 담고 있음
    # DRF 사용 시 Serializer에서 context["request"]를 받아서 사용했다면,
    # Strawberry에서는 strawberry.types에서 Info를 받아서 사용
    # parameter에 :Info 타입을 지정해주는 순간 Strawberry가 자동으로 StrawberryDjangoContext를 넣어줌!!!
    # 어느 자리에 넣어주는 지는 중요하지 않음. Info 타입을 지정하는 것이 중요!!!
    def is_owner(self, info: Info) -> bool:
        # print(info.context)
        # # StrawberryDjangoContext(request=<WSGIRequest: POST '/graphql'>, response=<TemporalHttpResponse status_code=None, "application/json">)
        # # request 객체가 출력되는 것을 확인할 수 있음
        # print(info.context.request.user)
        # # verobeach7
        return self.owner == info.context.request.user

    # Dynamic Field
    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            # self는 현재 처리 중인 room임을 잊지 말기
            rooms__pk=self.pk,
        ).exists()
