from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    Default user serializer
    Separated from register serializer so we can add/remove fields without causing security risks or break registration
    Combining these two might also lead to more complexity for any changes in the future
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name'
        )


class RegisterSerializer(ModelSerializer):
    password = CharField(required=True, write_only=True, min_length=8, max_length=32)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'email': {'required': True}}  # Django allows users with email=None, We want it required

    @staticmethod
    def validate_email(value):
        """
         Django User model allows duplicate emails.
         We want emails to be unique
        """
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("email already exists")

        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        # It's a good idea to add some validations for passwords
        # But we'll accept anything for now since we have limited time
        user.set_password(validated_data["password"])
        user.save()
        return user
