from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


# 같은 파일 내에서 사용하기 위해서는 먼저 정의되야 함
class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    # owner를 확장할 일이 있다면 TinyUserSerializer를 사용하라고 말해주면 됨
    # `read_only=True`설정을 하면 serializer는 owner에 대한 정보를 요구하지 않음
    # 사용자가 직접 기입하는 것을 막고 싶을 때 read_only=True를 설정해주면 됨
    owner = TinyUserSerializer(read_only=True)
    # 여러 개가 존재하는 경우 이를 알려줘야 함: many=True
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1

    # 내부 코드를 보여주기 위한 것. 알아서 아래처럼 처리함
    # def create(self, validated_data):
    #     # create 메서드의 반환 값은 항상 모델의 instance여야 함!!!
    #     return Room.objects.create(**validated_data)


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
