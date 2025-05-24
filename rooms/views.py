from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def say_hello(request):
    print(
        "request", request
    )  # 요청하고 있는 사용자 및 브라우저 정보, 전송하고 있는 데이터, 요청한 url 정보, ip정보, 쿠키 등을 담고 있음
    # return "hello"  # Error: 'str' object has no attribute 'get' -> HTTP Response를 Return해야 함
    return HttpResponse("hello")
