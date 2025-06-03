from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    # Wishlists는 본인만 볼 수 있어야 하기 때문에 본인의 자격 증명이 있어야만 진행할 수 있도록 함
    permission_classes = [IsAuthenticated]

    # 로그인한 유저가 생성한 위시리스트만 조회: filter
    def get(self, request):
        # filtering을 통해 내 wishlists만 가져오기
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            # WishlistSerializer를 호출하면 WishlistSerializer에서 RoomListSerializer를 호출하는데 RoomListSerializer의 is_owner field가 동적으로 처리되기 위해서는 context에 request가 필요함
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()가 호출될 때 WishlistSerializer의 모델을 받음
            # wishlist를 저장할 때 name과 user는 반드시 있어야 함. user는 사용자에게 입력받지 않고 request.user를 이용해 전달
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    # 인증 받지 않으면 진행할 수 없도록 IsAuthenticated 설정
    permission_classes = [IsAuthenticated]

    # Wishlist는 Private으로 본인만 권한을 가져야 함
    # get_object를 요청하는 곳에서 user 정보를 함께 보내야 함
    def get_object(self, pk, user):
        try:
            # 유저는 url로 요청하고 있는 유저와 같아야 함
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # permission_classes를 통과했으므로 request.user를 신뢰할 수 있음
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    # PUT Request는 Wishlist의 name만 변경 가능
    # rooms가 read_only이기 때문에 rooms를 수정하기 위해서는 별도의 rooms 수정 URL을 둬야 함
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)  # OBJECT
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )  # JSON
        if serializer.is_valid():
            wishlist = serializer.save()  # OBJECT
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},
            )  # JSON
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)


class WishlistRoomToggle(APIView):
    # 현 유저가 가지고 있는 wishlist 중에서 원하는 리스트를 가져옴
    def get_list(self, pk, user):
        try:
            # 유저는 url로 요청하고 있는 유저와 같아야 함
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    # 수정하기 원하는 방을 찾아옴
    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)

        # wishlist 안에 찾아온 room이 있는지 여부를 확인해야 함
        # room이 있는지 확인하기 위해서 모든 rooms를 불러와야 하는가?
        # if room in wishlist.rooms.all():
        # filter()를 사용하면 DB에서 있는지 여부만 확인 가능
        # if wishlist.rooms.filter(pk=room.pk): # 찾은 방들의 데이터를 리스트로 반환함

        ### ManyToManyField이기 때문에 장고에서 메서드를 제공: exists, all, filter, add, remove, clear, set 등
        # 존재 여부만 확인하고 싶다면 .exists()를 사용
        if wishlist.rooms.filter(pk=room.pk).exists():  # True or False
            # 존재한다면 wishlist에서 해당 room을 제거
            wishlist.rooms.remove(room)
        else:
            # 존재하지 않으면 wishlist에 해당 room 추가
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
