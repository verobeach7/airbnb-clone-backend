from rest_framework import serializers


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
    kind = serializers.CharField(
        max_length=15,
    )
    created_at = serializers.DateTimeField(
        read_only=True,
    )
