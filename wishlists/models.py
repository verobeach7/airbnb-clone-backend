from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
        blank=True,
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
        blank=True,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="wishlists",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name
