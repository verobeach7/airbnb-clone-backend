import strawberry
import typing
from . import types
from . import queries
from . import mutations
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    # Room Model이 아닌 Strawberry Extension이 Django의 모델을 보고 만들어 준 RoomType을 사용
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
        # 원하는 대로 permission을 설정해주면 됨
        permission_classes=[OnlyLoggedIn],
    )
    # typing.Optional 설정을 해주면 RoomType 객체가 있을 수도 없을 수도 있다는 것
    # 이 설정을 하면 GraphQL View에서 RoomType!에 !가 사라진 것을 확인할 수 있음
    # 즉, 반드시 RoomType을 받는 것은 아니라는 것
    # 하지만 queries.py에서 실제로 RoomType아 아닐 때 어떻게 할 것인지 추가 코딩을 해줘야 함
    room: typing.Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )


@strawberry.type
class Mutation:
    add_room: typing.Optional[types.RoomType] = strawberry.mutation(
        resolver=mutations.add_room,
        permission_classes=[OnlyLoggedIn],
    )
