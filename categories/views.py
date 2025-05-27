from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Django REST Framework를 사용하기 위해서 데코레이터만 달아주면 됨
@api_view()
def categories(request):
    return Response(
        {
            "ok": True,
            "categories": Category.objects.all(),
        }
    )
