from django.contrib import admin
from .models import Room, Amenity
from categories.models import Category


# Step1. Make action
@admin.action(description="Set all prices to zero")
# 3개의 parameters가 반드시 필요함
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    # Step2. Link actions
    # action을 연결하기 위해서는 actions에 만들어 놓은 action을 튜플로 넣어주면 됨
    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        # 여기에 추가되는 것을 장고는 모델에서 찾으려고 함
        # attribute을 찾아보고 없다면 method를 찾아봄
        "total_amenities",
        "rating",
        "owner",
        "created_at",
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
    # search_fields=는 List 또는 Tuple을 받음
    search_fields = (
        # search_fields는 기본으로 __contains로 검색
        # 만약 2를 검색하면 2, 20, 12 등 2를 포함하기만 하면 다 찾아옴
        "name",  # 1순위로 검색
        "price",  # 2순위로 검색(1순위 검색 후 없으면)
    )

    # 아래 코드를 이용하면 Rooms와 관련된 카테고리만 보여지게 할 수 있음
    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(kind="rooms")
        return form

    # # 방법2. 관리자 코드에 method 추가
    # def total_amenities(self, room):
    #     # print(self)  # rooms.RoomAdmin
    #     # print(room)  # APT in 서울
    #     # return "hi"
    #     return room.amenities.count()

    # # 방법1과 방법2가 모두 코딩 되어있는 경우 관리자 코드(방법2)가 우선함


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
