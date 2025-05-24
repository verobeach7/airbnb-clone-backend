from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def see_all_rooms(request):
    return HttpResponse("see all rooms")


# url에서 parameter를 받으므로 받아 줄 공간을 만들어야 함. room_id 추가
def see_one_room(request, room_id):
    return HttpResponse(f"see room with id: {room_id}")
