import strawberry
from strawberry import auto
import strawberry.django
from . import models


@strawberry.django.type(models.Review)
class ReviewType:
    id: auto
    payload: auto
    rating: auto
