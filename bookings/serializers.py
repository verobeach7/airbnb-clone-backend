from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    # 모델에서 null=True로 되어있는데 예약시 experience_time은 필수 필드이므로 overriding을 통해 필수 필드로 덮어쓰기
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


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

    # data에 모든 fields를 받아 한꺼번에 validate 할 수 있음
    def validate(self, data):
        # print(data)
        # {'check_in': datetime.date(2025, 6, 4), 'check_out': datetime.date(2025, 6, 5), 'guests': 2} -> data는 dictionary로 전달됨
        # check_in이 check_out보다 반드시 빨라야 함
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out.",
            )  # non_field_errors
        # 10-01~10-10 예약을 희망, 10-05~10-07 예약이 이미 있는 경우 예약 불가
        # 하지만 10-05~10-30 예약이 이미 있는 경우 예약 가능
        # 즉, 내가 예약을 희망하는 기간 사이에 정확히 들어가 있는 예약만 찾아낼 수 있음
        # Booking.objects.filter(
        #     # gte: 이후이거나 같은 때, lte: 이전이거나 같은 때
        #     check_in__gte=data["check_in"],
        #     check_out__lte=data["check_out"],
        # ).exists()

        # 1=======5
        #   2=3 불가
        #       4====6 불가
        #                8================15 가능
        #            6=====9 불가
        #            6===8 가능
        #         5==6 가능
        # 체크아웃 전에 체크인을 하고, 체크인 후에 체크아웃을 하는 기존 예약이 있는지 찾기
        if Booking.objects.filter(
            room=self.context["room"],
            # 기존 예약의 체크인이 새로운 예약의 체크아웃보다 빠른 게 있는지 확인
            check_in__lt=data["check_out"],  #  8 lt(<) 9
            # 기존 예약의 체크아웃이 새로운 예약의 체크인보다 늦는 게 있는지 확인
            check_out__gt=data["check_in"],  #  15 gt(>) 6
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        # data를 return한다는 것은 모든 validation을 통과했다는 의미
        return data


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
