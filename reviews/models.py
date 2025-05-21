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

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
