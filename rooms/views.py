import time
from django.conf import settings

# 파이썬 표준 라이브러리의 datatime을 사용할 수도 있지만 장고의 timezone은 config/settings.py의 설정을 활용할 수 있음
# import datetime
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category

# from reviews.serializers import ReviewSerializer
from reviews import serializers as ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        # print(serializer.data)
        # [{'id': 1, 'created_at': '2025-05-17T11:59:41.156367+09:00', 'updated_at': '2025-05-17T11:59:41.156382+09:00', 'name': '여행 가방 보관 가능', 'description': '체크인 시간보다 일찍 도착하거나 체크아웃 후 짐 보관을 원하는 게스트를 위한 서비스'}, {'id': 2, 'created_at': '2025-05-17T12:00:08.629960+09:00', 'updated_at': '2025-05-17T12:00:08.629986+09:00', 'name': '장기 숙박 가능', 'description': '28일 이상 숙박 가능'}, {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:28:09.479454+09:00', 'name': '디지털도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}]
        return Response(serializer.data)

    def post(self, request):
        # print("request.data", request.data)
        # request.data {'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}
        serializer = AmenitySerializer(data=request.data)
        # print("serializer", serializer)
        # serializer AmenitySerializer(data={'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            amenity = serializer.save()
            # print("amenity", amenity)
            ### Python Object
            # amenity 멋진 뒷뜰
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        # print("amenity", amenity)
        ### Python Object
        # amenity 멋진 도어록
        serializer = AmenitySerializer(amenity)
        # print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        # print("serializer.data", serializer.data)
        # JSON 변환됨
        # serializer.data {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:20:35.069248+09:00', 'name': '멋진 도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}
        return Response(serializer.data)
        # return Response(
        #     AmenitySerializer(self.get_object(pk)).data,
        # )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        # print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>, data={'name': '디지털도어록'}, partial=True):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            # print("updated_amenity", updated_amenity)
            # Python Object
            # updated_amenity 멋진 도어록
            # print("after serializing", AmenitySerializer(updated_amenity).data)

            # after serializing {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:20:35.069248+09:00', 'name': '멋진 도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")

            if not category_pk:
                raise ParseError(
                    "Category is required.",
                )
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'.")
            except Category.DoesNotExist:
                raise ParseError("category not found.")
            # transaction 없이는 코드를 실행할 때마다 쿼리가 즉시 데이터베이스에 반영됨
            # transaction을 사용하면 각 과정의 변경사항을 리스트로 저장해 놓음
            # transaction 내부의 모든 코드를 살펴본 후 에러가 발생하지 않는다면 DB로 푸쉬함
            # try-except가 있으면 transaction이 에러가 있음을 알기 전에 종료되버림
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(
                        room,
                        # RoomDetailSerializer 내부에서 SerializerMethodField를 호출할 때 request를 필요로 하므로 여기서 request를 포함하여 보내줘야 함
                        context={
                            "request": request,
                        },
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # time.sleep(1)
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            # context에 원하는 어떤 데이터든지 담아서 Serializer에 보낼 수 있음
            # context={"hello": "bye bye"},
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:
            raise PermissionDenied

        # Challenge
        serializer = RoomDetailSerializer(
            room,
            request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")

            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except Category.DoesNotExist:
                    raise ParseError("category not found.")

            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(
                            category=category,
                        )
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    serializer = RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception as e:
                raise ParseError(f"Error occurred: {e}")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)

        # elif: 이것을 사용하면 첫 번재 if를 통과하지 못하는 경우 거기서 끝나게 됨
        # 두 조건을 모두 검증하기 원한다면 별도의 if로 만들어줘야 함
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # time.sleep(1)
        try:
            # 모든 딕셔너리의 get Method는 기본값을 지정할 수 있음
            page = request.query_params.get("page", 1)
            # print(type(page))
            # parameter로 page를 줬을 때는 <class 'str'>, 기본값이 들어갈 때는 <class 'int'>로 타입이 결정됨
            # print(page)
            page = int(page)
        # page가 없거나 문자가 들어가는 경우 에러가 발생하는데 이 때 1페이지를 보여주도록 함
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer.ReviewSerializer(
            # 앞의 것(0)은 포함(inclusive)되고 뒤의 것(3)은 포함되지 않음(exclusive)
            # lazy하기 때문에 장고는 limit과 offset을 포함하는 SQL문을 DB에 보냄
            # 즉, 모든 데이터를 불러와 자르는 것이 아니라 해당되는 데이터만 불러옴
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer.ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                # 이미 user와 room에 대한 정보를 가지고 있음. 함께 보내기!
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer.ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            # 지금 이대로 serializer를 저장하면 PhotoSerializer는 pk, file(url), description만 가지고 있기 때문에 room에 해당하는지 experience에 해당하는지 알지 못 함

            photo = serializer.save(
                room=room,
            )
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    # get은 누구나 접근, post, put, delete은 인증된 사용자만 접근
    permission_classes = [IsAuthenticatedOrReadOnly]

    ### 방법1. 사용자가 예약하려고 하는 방이 존재하지 않는 경우 이를 알려주고 싶다면 이 방법을 사용
    # 이 방법은 DB를 2번 조회해야 하는 방법
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)  # 조회1
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        # timezone.now()는 서버의 로컬타임이 아닌 표준시를 가져옴
        # now = timezone.now()
        # 서버의 로컬타임을 가져오기 위해서 .localtime을 이용하면 됨
        # print(timezone.localtime(now))
        # .date()은 날짜 부분만 가져옴
        now = timezone.localtime(timezone.now()).date()
        # now=timezone.localdate(timezone.now()) # 위와 동일
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gte=now,
        )  # 조회2
        # 챌린지: bookings를 한번 더 필터링하여 url로 월을 보내게 하여 그 월에 해당하는 것만 보여주도록 하기
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    #         room__pk=pk
    ### 방법2. 존재하는 방에 대한 Booking을 찾아볼 것이라 믿으면 이 방법 사용
    # # 위처럼 복잡하게 처리하지 않아도 bookings를 찾을 수 있음: pk를 이용
    # # 하지만 방이 존재하지 않아도, 예약이 존재하지 않아도 같은 결과값을 가짐
    # # 그로 인해 방이 존재하지 않는 상황에서도 예약이 실패했다고 생각하게 됨
    # def get(self, request, pk):
    #     # Relationship을 바탕으로 filtering 할 때는 room을 먼저 찾을 필요 없이 바로 __를 이용하여 접근하면 됨
    #     bookings = Booking.objects.filter(
    #     )  # 만약 room에 예약이 없으면 결과 값은 빈 QuerySet이 됨
    #     # pk에 해당하는 room이 없으면 결과 값은 빈 List가 됨

    def post(self, request, pk):
        pass


class RoomMonthlyBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # 현재시간
        now = timezone.localtime(timezone.now()).date()
        # 년도와 월 정보를 query_params로 받아온다
        try:
            month = int(request.query_params.get("month", now.month))
            year = int(request.query_params.get("year", now.year))
            if year < now.year:
                year = now.year
                month = now.month
            elif (year == now.year) and (month < now.month):
                month = now.month

        except:
            month = now.month
            year = now.year

        search_date_start = now.replace(
            year=year,
            month=month,
            day=1,
        )
        print(search_date_start)

        next_month = month + 1 if month < 12 else 1
        next_month_year = year if month < 12 else year + 1
        search_date_end = now.replace(
            year=next_month_year,
            month=next_month,
            day=1,
        )

        # pagination
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            # check_in 날짜가 (우리가 있는 곳의) 현재 날짜보다 큰 booking을 찾고 있음
            check_in__gte=search_date_start,
            check_in__lt=search_date_end,
        )
        serializer = PublicBookingSerializer(
            # 해당 월 한번에 보여주기
            # bookings,
            # pagination
            bookings.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        # 예약 전 필요한 fields와 validation을 위한 Serailizer
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            # # request.data로부터 check_in 날짜를 받아옴
            # check_in=request.data.get("check_in")
            # # if-else로 오늘 이후의 예약인지 검증
            # 위 방법은 좋은 방법이고 잘 작동함

            # 다른 방법도 있음: Serializer의 validation을 커스텀하는 방법
            # Serializer에 직접 검증 코드를 추가할 수 있음: serializers.py 확인해보기
            booking = serializer.save(
                # CreateRoomBookingSerailizer에는 check_in, check_out, guests field만 있으므로 추가적으로 데이터를 보내줘야 함
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            # 생성된 예약을 보여주기 위한 Serailizer
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
