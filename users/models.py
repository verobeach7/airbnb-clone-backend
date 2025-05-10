from django.db import models

# Django가 기본으로 제공하는 User 모델을 상속받기 위해 Import
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 옵션을 선택하고 싶은 경우 클래스를 생성하여 튜플로 넣어줌
    class GenderChoices(models.TextChoices):
        MALE = (
            "male",
            "Male",
        )  # Tuple로 작성: 첫 번째는 데이터베이스에 기록될 데이터, 두 번째는 관리자 페이지에서 보여질 Lable을 넣어주면 됨
        FEMALE = (
            "female",
            "Female",
        )

    class LanguageChoices(models.TextChoices):
        KR = "kr", "Korean"  # python에서 Tuple은 ()를 생략해도 됨
        EN = "en", "English"

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    # AbstractUser의 내용을 Overriding
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.ImageField(
        blank=True,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,  # .choices를 붙여주면 클래스에서 상속받은 TextChoices를 사용하게 됨
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
