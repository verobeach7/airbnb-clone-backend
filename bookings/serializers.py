from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    # Overriding을 통해 check_in과 check_out을 필수로 만들어 줌
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        # 사용자에게 Request로 받을 fields만 추가
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # validate하고 싶은 field를 아래와 같이 메서드명으로 만들어주면 됨
    def validate_check_in(self, value):
        # print(value)  # value에는 check_in에 넘어온 값이 들어감
        # print(type(value)) # <class 'datetime.date'> serializers.DateField로 설정하였기 때문에 value는 data 타입임
        now = timezone.localdate(timezone.now())
        if now > value:
            # ValidationError를 발생시키면 검증에 실패함
            raise serializers.ValidationError("Can't book in the past!")
        # value를 성공적으로 반환하면 검증이 잘 완료된 것으로 간주함
        return value

    def validate_check_out(self, value):
        now = timezone.localdate(timezone.now())
        if now >= value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


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
