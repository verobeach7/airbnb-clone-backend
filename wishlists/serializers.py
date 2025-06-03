from rest_framework.serializers import ModelSerializer

# Wishlist에 보여줄 방들의 대략적인 정보를 가져오면 됨
from rooms.serializers import RoomListSerializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):
    # Wishlist를 만들 때 방 없이도 생성할 수 있도록 read_only=True 설정
    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
