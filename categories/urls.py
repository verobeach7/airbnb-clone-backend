from django.urls import path
from . import views

urlpatterns = [
    # path("", views.categories),
    # 클래스를 이용하는 것으로 변경해줘야 함
    # .as_view()를 붙이는 것은 단지 클래스를 가져오기 위한 규칙일 뿐임
    # .as_view()가 하는 일은 get과 post에 따라 Method를 작동시키기 위한 것
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]
