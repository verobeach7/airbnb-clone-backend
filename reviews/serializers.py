from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # Review를 POST할 때는 user 정보를 모두 다 기입해줄 필요가 없으며 사용자를 믿을 수도 없음
    # read_only=True 설정을 통해 GET할 때만 User에 대한 세부 정보를 가져오게 함
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
