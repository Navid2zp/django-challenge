from django.urls import path

from .views import StadiumAPI

app_name = "stadiums-api"

urlpatterns = [
    path('', StadiumAPI.as_view(), name='create-list'),
]
