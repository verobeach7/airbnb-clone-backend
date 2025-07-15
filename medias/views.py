import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


# Cloudflare에서 one-time upload url 가져오기
class GetUploadURL(APIView):
    # https://developers.cloudflare.com/images/upload-images/direct-creator-upload/
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ACCOUNT_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"}
        )
        # json으로 변환
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        # result에 있는 id와 uploadURL을 모두 프론트엔드가 받아야 함
        # uploadURL은 이미지를 탑재하는 데 사용
        # id는 해당 이미지를 가져와야 할 때 사용
        return Response({"result": result})
