from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    # 임시방편으로 ROOMS에 해당하는 카테고리만 가져오기
    # 나중에 제대로 처리해야 함
    # 두 개의 URL을 별도로 만들어줘야 함: 하나는 Rooms 카테고리 가져오기, 다른 하나는 EXPERIENCE 카테고리 가져오기
    queryset = Category.objects.filter(
        kind=Category.CategoryKindChoices.ROOMS,
    )
