from rest_framework import serializers
from .models import Booking


# 모든 사람이 방이나 체험에 예약이 어떻게 잡혀있는지 확인하기 위하여 사용하는 serializer
class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
