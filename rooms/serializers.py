from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


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
    # amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    # models.py의 rating Method를 이용하여 결과를 넣어 필드를 만들어 줌
    # 모델에 있는 속성 명 외 다른 이름을 사용해주면 됨. 겹치면 overriding되버림
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1

    # 반드시 get_{속성명}으로 이름지어줘야 모델의 메서드에서 계산한 결과가 rating에 들어감
    def get_rating(self, room):
        # veiws.py에서 context에 담아 보낸 데이터를 Serializer의 self.context로 받아서 사용할 수 있음
        # print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user  # True or False

    # 데이터베이스에 추가되는 것을 막기 위해 일부러 에러 발생시키기
    # def create(self, validated_data):
    #     # views.py에서 serializer.save(추가 데이터)에서 넘어온 최종 데이터 확인
    #     print(validated_data)
    #     # {'name': 'APT in 서울', 'country': '한국', 'city': '서울', 'price': 0, 'rooms': 12, 'toilets': 12, 'description': 'ㅁㄴㅇㄹ', 'address': '서울', 'pet_friendly': True, 'kind': 'entire_place', 'owner': <SimpleLazyObject: <User: verobeach7>>}
    #     return

    # 내부 코드를 보여주기 위한 것. 알아서 아래처럼 처리함
    # def create(self, validated_data):
    #     # create 메서드의 반환 값은 항상 모델의 instance여야 함!!!
    #     return Room.objects.create(**validated_data)

    # room은 Serializer에서 serializing하고 있는 room
    def get_is_liked(self, room):
        # views.py에서 RoomDetailSerializer 호출 시 함께 보낸 context
        request = self.context["request"]
        # 현 유저의 모든 wishlists를 가져오기 위함, 두 번째 인자는 현재 Room이 유저의 wishlist에 있는지 확인하기 위한 것
        # __ 이용
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
            # rooms가 가지고 있는 property를 이용할 수 있음
            # rooms__name="big tent",
        ).exists()


class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
