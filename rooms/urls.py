from django.urls import path
from . import views  # 현재 폴더 내에서 views.py를 import

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/bookings", views.RoomBookings.as_view()),
    path("<int:pk>/bookings/check", views.RoomBookingCheck.as_view()),
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
