from .models import Category
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            # all_categories는 QuerySet으로 JSON으로 serialize 필요
            "categories": serializers.serialize("json", all_categories),
        }
    )
