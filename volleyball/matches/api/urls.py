from django.urls import path

from .views import MatchAPI, MatchAddSeatAPI

app_name = "matches-api"

urlpatterns = [
    path('', MatchAPI.as_view(), name='create-list'),
    path('<int:match_id>/addSeats/', MatchAddSeatAPI.as_view(), name='add-seats'),
]
