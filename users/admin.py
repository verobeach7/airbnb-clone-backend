from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
# 이 클래스가 User 모델을 관리한다고 알려줘야 함
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
