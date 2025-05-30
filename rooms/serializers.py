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
    owner = TinyUserSerializer()
    # 여러 개가 존재하는 경우 이를 알려줘야 함: many=True
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1


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
