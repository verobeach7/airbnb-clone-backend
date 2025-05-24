"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

# ### 방법 1. 이 경우 메소드명이 중복되어 문제가 될 수 있음
# from rooms.views import say_hello
# from users.views import say_hello

# urlpatterns = [
#     # url에 admin으로 접근하면 admin.site.urls 함수를 작동시킴
#     path("admin/", admin.site.urls),
#     path("rooms", say_hello),
#     path("users", say_hello),
# ]

# ### 방법 2. 이 경우 views라는 파일명이 중복되게 됨
# from rooms import views
# from users import views

# urlpatterns = [
#     # url에 admin으로 접근하면 admin.site.urls 함수를 작동시킴
#     path("admin/", admin.site.urls),
#     path("rooms", views.say_hello),
#     path("users", views.say_hello),
# ]

# ### as를 이용하여 별칭을 붙여 해결 가능
# from rooms import views as rooms_views
# from users import views as users_views

# urlpatterns = [
#     # url에 admin으로 접근하면 admin.site.urls 함수를 작동시킴
#     path("admin/", admin.site.urls),
#     path("rooms", rooms_views.say_hello),
#     path("users", users_views.say_hello),
# ]

from rooms import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # 여기에 path를 넣어줘야만 장고가 해당 url에 따른 함수를 실행하여 view를 보여줌
    path("rooms", views.say_hello),
]
