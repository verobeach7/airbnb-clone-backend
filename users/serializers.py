from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        # password의 Hash 값은 사용자 본인에게도 보여줄 필요가 없음
        # 관리자만 관리할 수 있는 부분은 사용자가 수정할 수 없도록 해야 함
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "id",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    roomsCount = SerializerMethodField()
    reviewsCount = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "avatar",
            "name",
            "gender",
            "username",
            "roomsCount",
            "reviewsCount",
        )

    def get_roomsCount(self, user):
        return user.rooms.count()

    def get_reviewsCount(self, user):
        return user.reviews.count()
