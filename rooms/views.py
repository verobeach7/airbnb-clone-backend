from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def see_all_rooms(request):
    rooms = Room.objects.all()
    # render의 첫 번째 인자: request
    # render의 두 번째 인자: 템플릿
    # render의 세 번째 인자: context - html 페이지로 보낼 데이터(딕셔너리 형태의 {Key: Value}로 보냄)
    return render(
        request,
        "all_rooms.html",
        {"rooms": rooms, "title": "this title comes from django"},
    )


# url에서 parameter를 받으므로 받아 줄 공간을 만들어야 함. room_id 추가
def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {"room": room},
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {"not_found": True},
        )
