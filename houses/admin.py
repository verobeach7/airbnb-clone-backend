from django.contrib import admin
from .models import House


# Register your models here. 여기에 등록하면 Admin Panel에 나타남.
# Decorator: 이 클래스가 admin하게 될 model이 house라고 알려주는 것
# 즉, 이 클래스가 House Model을 컨트롤 함
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):  # ModelAdmin을 상속받음. ModelAdmin은 Admin Panel임
    # # Admin Panel에 보이고 싶은 Column들을 list에 넣어주면 됨
    # # list에는 당연히 Model에 명시한 property 이름을 그대로 넣어줘야 함
    # list_display = ["name", "price_per_night", "address", "pets_allowed"]
    # # list_filter를 이용하면 필터링 기능을 사용할 수 있음
    # list_filter = ["price_per_night", "pets_allowed"]
    # # Admin Panel에 검색 기능을 추가함
    # # search_fields = ["address"] # address 컬럼에서 검색
    # search_fields = ["address__startswith"] # 기입한 문자로 시작하는 것을 검색

    # List보다 Tuple을 사용하는 것을 더 권장: Immutable하기 때문
    list_display = ("name", "price_per_night", "address", "pets_allowed")
    list_filter = ("price_per_night", "pets_allowed")
    # Tuple 안에 한 개의 요소만 있을 때는 반드시 ,를 이용해줘야 함
    # ,를 사용하지 않으면 파이썬이 괄호를 없애고 문자열로 바꿔버림
    search_fields = ("address__startswith",)
