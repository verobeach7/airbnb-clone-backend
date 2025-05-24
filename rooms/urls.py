from django.urls import path
from . import views  # 현재 폴더 내에서 views.py를 import

urlpatterns = [
    # "": 이미 config/urls.py에서 rooms 경로로 들어와 있기 때문에 ""은 rooms의 root에 해당
    path("", views.see_all_rooms),
    # url에서 변수 받는 법: 변수가 들어가는 자리에 <Type:parameter_name>을 넣어주면 됨
    path("<int:room_id>", views.see_one_room),
]
