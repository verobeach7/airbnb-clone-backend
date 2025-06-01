from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        print(serializer.data)
        # [{'id': 1, 'created_at': '2025-05-17T11:59:41.156367+09:00', 'updated_at': '2025-05-17T11:59:41.156382+09:00', 'name': '여행 가방 보관 가능', 'description': '체크인 시간보다 일찍 도착하거나 체크아웃 후 짐 보관을 원하는 게스트를 위한 서비스'}, {'id': 2, 'created_at': '2025-05-17T12:00:08.629960+09:00', 'updated_at': '2025-05-17T12:00:08.629986+09:00', 'name': '장기 숙박 가능', 'description': '28일 이상 숙박 가능'}, {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:28:09.479454+09:00', 'name': '디지털도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}]
        return Response(serializer.data)

    def post(self, request):
        print("request.data", request.data)
        # request.data {'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}
        serializer = AmenitySerializer(data=request.data)
        print("serializer", serializer)
        # serializer AmenitySerializer(data={'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            amenity = serializer.save()
            print("amenity", amenity)
            ### Python Object
            # amenity 멋진 뒷뜰
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        print("amenity", amenity)
        ### Python Object
        # amenity 멋진 도어록
        serializer = AmenitySerializer(amenity)
        print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        print("serializer.data", serializer.data)
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
        print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>, data={'name': '디지털도어록'}, partial=True):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            print("updated_amenity", updated_amenity)
            # Python Object
            # updated_amenity 멋진 도어록
            print("after serializing", AmenitySerializer(updated_amenity).data)

            # after serializing {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:20:35.069248+09:00', 'name': '멋진 도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
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
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
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

        if not request.user.is_authenticated:
            raise NotAuthenticated
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
        if not request.user.is_authenticated:
            raise NotAuthenticated
        # elif: 이것을 사용하면 첫 번재 if를 통과하지 못하는 경우 거기서 끝나게 됨
        # 두 조건을 모두 검증하기 원한다면 별도의 if로 만들어줘야 함
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            # 모든 딕셔너리의 get Method는 기본값을 지정할 수 있음
            page = request.query_params.get("page", 1)
            print(type(page))
            # parameter로 page를 줬을 때는 <class 'str'>, 기본값이 들어갈 때는 <class 'int'>로 타입이 결정됨
            print(page)
            page = int(page)
        # page가 없거나 문자가 들어가는 경우 에러가 발생하는데 이 때 1페이지를 보여주도록 함
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            # 앞의 것(0)은 포함(inclusive)되고 뒤의 것(3)은 포함되지 않음(exclusive)
            # lazy하기 때문에 장고는 limit과 offset을 포함하는 SQL문을 DB에 보냄
            # 즉, 모든 데이터를 불러와 자르는 것이 아니라 해당되는 데이터만 불러옴
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
