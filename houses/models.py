from django.db import models


# Create your models here.
# models.Model을 상속받음
class House(models.Model):
    """Model Definition for Houses"""

    # CharField는 길이 제한이 있는 문자열 형태를 가질 때 사용
    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField()
    # TextField는 길이 제한이 없음
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True)

    # __str__()메서드 오버라이딩을 통해서 내가 원하는 모습으로 바꿔줄 수 있음
    def __str__(self):
        return self.name
