from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    """Photo Model Definition"""

    file = models.URLField()
    description = models.CharField(
        max_length=150,
    )
    # 사진은 room 또는 experience 둘 중 하나에 종속되기 때문에 둘 중 하나는 null이 될 수밖에 없음
    room = models.ForeignKey(
        "rooms.Room",
        related_name="photos",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="photos",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    """Video Model Definition"""

    file = models.URLField()
    # 비디오는 오직 한개만 탑재할 수 있기에 One to One Field를 사용
    # 외래키로 연결되지만 한 개만 고유하게 연결 가능함
    experience = models.OneToOneField(
        "experiences.Experience",
        related_name="videos",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Video File"
