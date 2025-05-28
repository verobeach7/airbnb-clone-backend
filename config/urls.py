from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # url에서 rooms로 접근하면 rooms/urls.py가 view를 처리
    # include를 이용하면 별도의 import가 불필요함
    # 파일 경로를 넣어주면 장고가 알아서 처리함
    # API 버져닝을 통해 관리: 추후 개선 작업 시 기존과 새로운 버전을 모두 활용 가능
    # 서버 작업과 API를 분리 가능
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
]
