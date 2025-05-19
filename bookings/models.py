from django.db import models
from common.models import CommonModel


class Booking(CommonModel):
    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    # Booking은 한 명의 예약자와 하나의 Room 또는 Experience가 필요함. One to Many 관계임.
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        # 방이 삭제되더라도 유저는 예약 기록을 가지고 있는 것이 여행 기록을 남길 수 있기에 좋음
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # check_in, check_out은 Room Booking에 사용
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    # experience_time은 Experience Booking에 사용
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    # guests는 Room과 Experience 예약 시 모두 필요
    guests = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.room if self.kind=="room" else self.experience}"
