from django.db import models

# Django가 기본으로 제공하는 User 모델을 상속받기 위해 Import
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
