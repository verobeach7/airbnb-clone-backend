import strawberry
import typing
from . import types
from . import queries


@strawberry.type
class Query:
    # Room Model이 아닌 Strawberry Extension이 Django의 모델을 보고 만들어 준 RoomType을 사용
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
    )
    room: types.RoomType = strawberry.field(
        resolver=queries.get_room,
    )
