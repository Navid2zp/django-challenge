from django.urls import path

from .views import StadiumAPI

app_name = "stadiums-api"

urlpatterns = [
    # path('<int:stadium_id>/seats/', StadiumSeatsAPI.as_view(), name='seats'),
    path('', StadiumAPI.as_view(), name='create-list'),
]
