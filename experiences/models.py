from django.db import models
from django.db.models import Avg
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
        default="",
    )
    host = models.ForeignKey(
        "users.User",
        related_name="experiences",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="experiences",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def rating(experience):
        average_rating = experience.reviews.aggregate(Avg("rating"))["rating__avg"]
        if average_rating is None:
            return 0
        else:
            return round(average_rating, 2)


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(max_length=100)
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
