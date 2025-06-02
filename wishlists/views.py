from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
