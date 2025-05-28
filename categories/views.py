from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer


# Django REST Framework를 사용하기 위해서 데코레이터만 달아주면 됨
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,  # Django Model을 JSON으로 변환
            many=True,
        )
        return Response(serializer.data)
    elif request.method == "POST":
        # 다음과 같이 진행하여 DB에 Category를 만들면 될 것 같지만 이렇게 하면 안됨
        # 어떠한 검증도 없이 사용자를 100% 신뢰한다는 것과 같음
        # 항상 Data를 검증해야 함!!!
        # 즉, 최소한 모델에서 설정한 규약을 준수하도록 해야 함: 문자 길이 등
        # 이대로 진행하면 사용자가 엄청 긴 텍스트를 보내는 경우 데이터베이스에서 에러 발생
        # Category.objects.create(
        #     name=request.data["name"],
        #     kind=request.data["kind"],
        # )
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)  # Django Model의 Instance를 가져옴
    serializer = CategorySerializer(category)  # 첫 번째 인자로 넣어주면 JSON으로 변환
    return Response(serializer.data)
