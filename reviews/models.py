from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    """Review from a user to Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reviews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="reviews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    # # 리뷰 리스트를 역순(최신순)으로 하고 싶으면 Meta class에 ordering을 설정해주면 됨
    # class Meta:
    #     ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
