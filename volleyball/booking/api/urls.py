from django.urls import path

from .views import SeatReservationAPI, ReservationVerificationAPI

app_name = "booking-api"

urlpatterns = [
    path('<int:seat_id>/book/', SeatReservationAPI.as_view(), name='reserve'),
    path('<int:seat_id>/book/verify/', ReservationVerificationAPI.as_view(), name='verify'),
]
