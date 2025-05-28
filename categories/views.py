from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
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
            # User로부터 온 JSON을 장고 모델로 변환한다는 것은 데이터베이스에 Category 추가를 의미
            # serializer.save() 호출 시 자동으로 serializer에서 create method를 찾음
            # 즉, CategorySerializer에 create Method를 만들어줘야 함
            new_category = (
                serializer.save()
            )  # 반환값인 new_category는 Django 모델(Python 객체)
            # 장고 모델 데이터를 다시 JSON으로 변경하여 브라우저에 반환하여 보여줌
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)  # Django Model의 Instance를 가져옴
    except Category.DoesNotExist:
        raise NotFound  # raise가 실행되면 이후의 코드는 실행되지 않음

    if request.method == "GET":
        serializer = CategorySerializer(
            category
        )  # 첫 번째 인자로 넣어주면 JSON으로 변환
        return Response(serializer.data)
    elif request.method == "PUT":
        # 데이터베이스에서 가져온 Django Model의 Instance와 User의 data를 함께 보내면 자동으로 UPDATE로 처리함
        serializer = CategorySerializer(
            category,
            data=request.data,
            # 저장되어 있는 데이터는 이미 유효성 검사를 거친 데이터이기 때문에 필수 데이터는 모두 들어가 있음
            # 이 상태에서 수정을 할 때는 수정할 데이터만 보내주면 됨
            # 아래 코드를 이용해 수정 작업에 해당하여 수정할 데이터만 보낸다는 것을 명시
            partial=True,
        )
        if serializer.is_valid():
            updated_category = (
                serializer.save()
            )  # PUT임을 인식하고 update Method를 실행함
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
