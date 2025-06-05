from rest_framework.response import Response
from rest_framework.views import APIView

# status 자체를 import하면 status를 타이핑하면 자동완성으로 한번에 볼 수 있음
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers


class Me(APIView):
    # 내 모든 정보는 Private이므로 IsAuthenticated 설정
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
