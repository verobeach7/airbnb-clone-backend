from django.contrib import admin
from .models import House


# Register your models here. 여기에 등록하면 Admin Panel에 나타남.
# Decorator: 이 클래스가 admin하게 될 model이 house라고 알려주는 것
# 즉, 이 클래스가 House Model을 컨트롤 함
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):  # ModelAdmin을 상속받음. ModelAdmin은 Admin Panel임
    # 클래스를 그대로 상속받아 사용하는 경우 pass만 적으면 됨
    pass
