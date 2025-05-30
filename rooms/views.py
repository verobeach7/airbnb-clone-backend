from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


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
        )
        return Response(serializer.data)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
