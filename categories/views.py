from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .serializers import CategorySerializer


# Django REST Framework의 APIView Class 사용
# 이 클래스에는 @api_view, if request.method를 이미 가지고 있음
# 클래스를 이용하면 if문을 이용하여 분기하지 않아도 됨
class Categories(APIView):
    # get, post method만 만들었기 때문에 알아서 둘만 작동함
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):

    # get_object()를 만들어서 get, put, delete에서 모두 사용할 수 있게 함
    # get_object()를 만드는 것이 규칙은 아님. 단지 DRF를 사용하는 관습, 관례.
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
