from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer


# Django REST Framework를 사용하기 위해서 데코레이터만 달아주면 됨
@api_view()
def categories(request):
    all_categories = Category.objects.all()
    # 그냥 all_categories만 넘기면 serializers.py에서는 하나의 category만 넘어오고 이것을 번역할 것이라고 생각함. 실은 여러 카테고리를 담고 있는 리스트가 보내지기 때문에 `many=True`를 함께 보내줘야 함.
    serializer = CategorySerializer(
        all_categories,
        many=True,
    )
    return Response(
        {
            "ok": True,
            # Response가 자동으로 Serializable하게 바꿔주지는 않음
            # Django Serialization Framework는 별로 좋지 않음
            # Django REST Framework와 함께 제공되는 Serializer를 사용하여 해결
            # 별도의 serializers.py 파일 생성 필요
            # "categories": Category.objects.all(),
            "categories": serializer.data,
        }
    )
