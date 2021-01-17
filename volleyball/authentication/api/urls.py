from django.urls import path

from authentication.api.views import RegisterView, LoginView

app_name = "auth-api"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
