from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    # Meta 설정만으로 장고가 모델을 위한 Serializer를 만들어 줌
    class Meta:
        model = Category
        # fields나 exclude 둘 중에 하나를 설정해주면 됨
        # fields는 어떤 field를 보이게 할 것인지 설정
        fields = (
            "name",
            "kind",
        )

        # exclude는 어떤 field를 가릴 것인지(보이지 않게 할 것인지) 설정
        # exclude = ("updated_at",)

        # 모든 fields를 보이게 하려면
        # fields = "__all__"
