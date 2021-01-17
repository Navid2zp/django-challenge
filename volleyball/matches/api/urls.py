from django.urls import path

from .views import MatchAPI, MatchAddSeatAPI, MatchSeatsAPI, MatchAvailableSeatsAPI

app_name = "matches-api"

urlpatterns = [
    # It might be a good idea to separate the endpoints for create and list.
    # We combined them for simplicity, reusability and since we know there won't be any changes in the future.
    path('', MatchAPI.as_view(), name='create-list'),
    path('<int:match_id>/seats/available/', MatchAvailableSeatsAPI.as_view(), name='available-seats'),
    path('<int:match_id>/seats/', MatchSeatsAPI.as_view(), name='seats'),
    path('<int:match_id>/addSeats/', MatchAddSeatAPI.as_view(), name='add-seats'),
]
