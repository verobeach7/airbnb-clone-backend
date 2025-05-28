from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    # 모델에 있는 속성을 다시 알려줘서 JSON으로 표현할 수 있도록 함
    # 모델에도 작성한 것을 다시 반복적으로 작성해야 해서 비효율적
    # 추후에 Django REST Framework를 사용하여 쉽게 해결할 것임

    # 여기에 작성한 것만 Serialize해서 JSON으로 보냄
    pk = serializers.IntegerField(
        read_only=True,
    )
    # pk = (
    #     serializers.CharField()
    # )  # 스트링으로 변환하여 보내게 됨. 즉, 원하는 형태로 데이터 타입도 수정 가능
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        # max_length=15, # ChoiceField이므로 글자수 제한 불필요
        choices=Category.CategoryKindChoices.choices,  # 선택지 외 불가 설정
    )
    created_at = serializers.DateTimeField(
        read_only=True,
    )

    def create(self, validated_data):
        # 아래처럼 Django Model로 만들어 줄 수 있음
        # 매우 큰 모델인 경우 아래처럼 일일이 다 해주는 것은 매우 비효율적
        # Property가 100개라면? 100개를 다 일일이 작성?
        # Category.objects.create(
        #     name=validated_data["name"],
        #     kind=validated_data["kind"],
        # )
        # DB에 유효성 검사를 마친 장고 모델 데이터를 가지고 데이터베이스에 새로운 카테고리를 생성함
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # if validated_data["name"]:
        #     instance.name = validated_data["name"]

        # validated_data는 Dictionary
        # Dictionary는 get 메서드를 가지고 있음
        # get 메서드는 첫 번째 인자로 키, 두 번째 인자는 키를 가지고 찾은 값이 없을 시 Default Value 지정
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
