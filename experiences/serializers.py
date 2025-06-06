from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Perk, Experience
from wishlists.models import Wishlist
from users import serializers as UserSerializer
from categories import serializers as CategorySerializer
from medias import serializers as MediaSerializer


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    host = UserSerializer.TinyUserSerializer(read_only=True)
    category = CategorySerializer.CategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = MediaSerializer.PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            experiences__pk=experience.pk,
        ).exists()


class ExperienceListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    photos = MediaSerializer.PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "host",
            "price",
            "address",
            "start",
            "end",
            "description",
            "perks",
            "rating",
            "is_host",
            "photos",
        )

    def get_rating(self, experience):
        # Experience Model의 rating() 메서드 사용
        return experience.rating()

    def get_is_host(self, expereince):
        # View에서 보내온 context를 활용
        request = self.context["request"]
        return expereince.host == request.user
