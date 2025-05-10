from django.db import models

# Django가 기본으로 제공하는 User 모델을 상속받기 위해 Import
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # AbstractUser의 내용을 Overriding
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
