from django.db import models


class CommonModel(models.Model):
    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django에서 Model을 Configure할 때 사용하는 클래스: Meta
    class Meta:
        # abstract를 True로 설정하면 Blueprint로써 사용하게 됨
        # 즉, 장고가 이 모델은 데이터베이스에 추가하는 것을 제외시킴!!!
        abstract = True
