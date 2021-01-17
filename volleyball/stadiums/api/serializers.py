from typing import Union

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from stadiums.models import Stadium, StadiumSeat


class StadiumSerializer(ModelSerializer):
    """ Serializer responsible for generating stadiums list and creating one"""

    class Meta:
        model = Stadium
        fields = (
            'id', 'name', 'capacity'
        )

        # add id to read_only_fields so we won't allow post data to include id
        # it will also notify swagger to exclude this field for post requests
        read_only_fields = ('id',)


class StadiumSeatSerializer(ModelSerializer):
    class Meta:
        model = StadiumSeat
        fields = (
            'id', 'seat_code', 'view'
        )
        read_only_fields = ('id',)

    def __get_stadium(self) -> Union[Stadium, None]:
        """
        Extract stadium from context

        :return: stadiums.models.Stadium object
        """
        return self.context.get('stadium')

    def validate_seat_code(self, value):
        """
        DRF doesn't validate unique_together or positive integer so we have to do it manually
        :param value: int - seat code
        :return: int - seat code
        :raise: ValidationError - if seat_code exists in the stadium or seat code is less than 1
        """

        if value < 1:
            raise ValidationError("seat code must be greater than 0")

        if StadiumSeat.objects.filter(
                seat_code=value,
                stadium=self.__get_stadium()
        ).exists() > 0:
            raise ValidationError("this seat code exists in this stadium")

        return value

    def create(self, validated_data):
        seat = StadiumSeat(**validated_data)

        # add the stadium object passed from view
        seat.stadium = self.__get_stadium()
        seat.save()
        return seat
