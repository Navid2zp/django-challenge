from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, RegisterSerializer


class RegisterView(CreateAPIView):
    """
    Register view for new users
    Uses RegisterSerializer for validations
    Serializer itself will raise exceptions in case any validations fail
    """

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        context = {
            'status': 'ok',
            'message': 'user registered',
            'user': UserSerializer(user).data
        }
        return Response(context, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        override perform_create to return user object. (default return is None)
        """

        return serializer.save()


class LoginView(APIView):
    """
    Login user and generate authentication token using username and password
    """

    authentication_classes = [BasicAuthentication]  # use BasicAuthentication to verify username and password
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def generate_expiry(get_query: dict) -> timezone.timedelta:
        """
        Generate expiration time delta based on `rememberme` GET query

        :param get_query: GET request
        :return: timezone.timedelta
        """
        remember = str(get_query.get('rememberme', False)).lower() == 'true'
        # 30 days if rememberme is true, 3 hours otherwise
        expiry = timezone.timedelta(days=30) if remember else timezone.timedelta(hours=3)
        return expiry

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="username", required=True, type="string", in_="authorization header"),
            openapi.Parameter(name="password", required=True, type="string", in_="authorization header")
        ],
        tags=["authentication"],
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response(
                description="credentials accepted",
                examples={
                    "application/json": {
                        "user": {
                            "id": 4,
                            "email": "test1@test.com",
                            "username": "test1",
                            "first_name": "name",
                            "last_name": "last name"
                        },
                        "token": "token_string"
                    }
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description="user object")
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """ Generate an auth token if username and password were valid. """

        _, token = AuthToken.objects.create(request.user, expiry=self.generate_expiry(request.GET))
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        context = {'request': self.request}
        return Response({
            'user': UserSerializer(request.user, context=context).data,
            'token': token,
        }, status=status.HTTP_202_ACCEPTED)
