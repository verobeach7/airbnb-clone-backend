from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    """Room or Experience Category"""

    # models.TextChoices를 이용하면 선택 옵션을 제공할 수 있음
    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=15,
        # 반드시 .choices를 붙여줘야 함
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        # kind는 문자열. 문자열은 .title() 메서드를 사용할 수 있음.
        # 제목으로 해주면 첫 글자를 대문자로 바꿔줌
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
