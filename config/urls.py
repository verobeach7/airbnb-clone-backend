from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # url에서 rooms로 접근하면 rooms/urls.py가 view를 처리
    # include를 이용하면 별도의 import가 불필요함
    # 파일 경로를 넣어주면 장고가 알아서 처리함
    path("rooms/", include("rooms.urls")),
    path("categories/", include("categories.urls")),
]
