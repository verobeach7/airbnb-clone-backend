from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# 장고는 프로젝트 내 어디서든 settings.py에 바로 접근할 수 있는 지름길을 제공
# settings.py에 대한 PROXY
# 즉, settings.py에는 장고를 설정하기 위한 것 뿐만 아니라 API Token이나 기타 설정 사항도 저장해놓고 쓸 수 있음
from django.conf import settings

# User에게 Strawberry API를 보여주기 위해서 GraphQLView를 임포트하여 사용
from strawberry.django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # url에서 rooms로 접근하면 rooms/urls.py가 view를 처리
    # include를 이용하면 별도의 import가 불필요함
    # 파일 경로를 넣어주면 장고가 알아서 처리함
    # API 버져닝을 통해 관리: 추후 개선 작업 시 기존과 새로운 버전을 모두 활용 가능
    # 서버 작업과 API를 분리 가능
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/users/", include("users.urls")),
    # GraphQLView에 Schema를 넘겨줘야 함
    path("graphql", GraphQLView.as_view(schema=schema)),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
