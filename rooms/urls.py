from django.urls import path
from . import views  # 현재 폴더 내에서 views.py를 import

urlpatterns = [
    # "": 이미 config/urls.py에서 rooms 경로로 들어와 있기 때문에 ""은 rooms의 root에 해당
    path("", views.say_hello),
]
