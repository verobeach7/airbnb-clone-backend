from django.urls import path
from . import views

urlpatterns = [
    # path("", views.categories),
    # 클래스를 이용하는 것으로 변경해줘야 함
    # .as_view()를 붙이는 것은 단지 클래스를 가져오기 위한 규칙일 뿐임
    # .as_view()가 하는 일은 get과 post에 따라 Method를 작동시키기 위한 것
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                # ViewSet의 Actions Method와 사용자가 보낼 HTTP Method를 연결해주면 됨
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        # 반드시 변수명을 'pk'로 해줘야 함
        # ModelViewSet 클래스의 메소드를 보면 이미 'pk'로 사전 설정되어 있음
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
