from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire Place"
        PRIVATE_ROOM = "private_room", "Private Room"
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        # room_set 대신에 rooms로 Reverse Accessors로 이용 가능
        # User.room_set.all() 대신 User.rooms로 접근
        # 더이상 room_set은 없어지며, rooms로 접근해야 함
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="rooms",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # 첫 번째 parameter 자리는 무조건 self이기 때문에 이름을 붙여줘도 self로 작동함
    def __str__(room) -> str:
        return room.name

    # # 방법1. 모델에 method를 추가
    # def total_amenities(self):
    #     print(self)
    #     return "hello"

    # 첫 번째 parameter 자리는 무조건 self이기 때문에 이름을 붙여줘도 self로 작동함
    def total_amenities(room):
        return room.amenities.count()


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,  # 추가해주지 않으면 null=True임에도 불구하고 Form Validation을 통과하지 못하기 때문에 에러가 발생됨
    )

    # 첫 번째 parameter 자리는 무조건 self이기 때문에 이름을 붙여줘도 self로 작동함
    def __str__(amenity) -> str:
        return amenity.name

    # Meta 정보를 수정
    class Meta:
        # verbose_name_plural: 복수형 일반화 오류가 발생하는 경우 바로 잡아 줄 수 있음
        verbose_name_plural = "Amenities"
