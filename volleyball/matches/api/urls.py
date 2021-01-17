from django.urls import path

from .views import MatchAPI

app_name = "matches-api"

urlpatterns = [
    path('', MatchAPI.as_view(), name='create-list'),
]
