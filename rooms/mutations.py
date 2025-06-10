from django.db import transaction
import strawberry
from strawberry.types import Info
import typing
from enum import Enum
from .models import Room, Amenity
from categories.models import Category


@strawberry.enum
class RoomKindChoices(Enum):
    ENTIRE_PLACE = "entire_place", "Entire Place"
    PRIVATE_ROOM = "private_room", "Private Room"
    SHARED_ROOM = "shared_room", "Shared Room"


def add_room(
    info: Info,
    name: str,
    price: int,
    rooms: int,
    toilets: int,
    description: str,
    address: str,
    pet_friendly: bool,
    kind: RoomKindChoices,
    amenities: typing.List[int],
    category_pk: int,
    country: typing.Optional[str] = "한국",
    city: typing.Optional[str] = "서울",
):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == category.CategoryKindChoices.EXPERIENCES:
            raise Exception("The category kind should be 'rooms'.")
    except Category.DoesNotExist:
        raise Exception("Category not found.")
    try:
        with transaction.atomic():
            room = Room.objects.create(
                name=name,
                country=country,
                city=city,
                price=price,
                rooms=rooms,
                toilets=toilets,
                description=description,
                address=address,
                pet_friendly=pet_friendly,
                kind=kind,
                owner=info.context.request.user,
                category=category,
            )

            for amenity_pk in amenities:
                amenity = Amenity.objects.get(pk=amenity_pk)
                room.amenities.add(amenity)

            room.save()

            return room

    except Exception as e:
        raise Exception(f"Amenity not found.: {e}")
