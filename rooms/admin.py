from django.contrib import admin
from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "price",
        "pet_friendly",
        "kind",
        "amenities",
        # 날짜로 필터를 사용하는 경우 장고가 알아서 오늘, 7일, 한달 등으로 알아서 필터링 해주는 기능을 가지고 있음
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    # 수정 가능한 필드에서 수정 불가능한 DB 데이터를 보여주기 위해 readonly_fields를 사용
    readonly_fields = (
        "created_at",
        "updated_at",
    )
