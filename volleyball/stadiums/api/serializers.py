from typing import Union

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from stadiums.models import Stadium, StadiumSeat


class StadiumSerializer(ModelSerializer):
    """ Serializer responsible for generating stadiums list and creating one"""

    class Meta:
        model = Stadium
        fields = (
            'id', 'name', 'row_count', 'seat_in_row'
        )

        # add id to read_only_fields so we won't allow post data to include id
        # it will also notify swagger to exclude this field for post requests
        read_only_fields = ('id',)

    def create(self, validated_data):
        stadium = Stadium(**validated_data)
        stadium.save()

        # These two methods should run in the background.
        stadium.create_rows()
        stadium.create_seats()
        return stadium


# class StadiumSeatSerializer(ModelSerializer):
#     class Meta:
#         model = StadiumSeat
#         fields = (
#             'id', 'view', 'seat_row', 'seat_column'
#         )
#         read_only_fields = ('id',)
#
#     def __get_stadium(self) -> Union[Stadium, None]:
#         """
#         Extract stadium from context
#
#         :return: stadiums.models.Stadium object
#         """
#         return self.context.get('stadium')
#
#     def create(self, validated_data):
#         if StadiumSeat.objects.filter(
#                 stadium=self.__get_stadium(),
#                 seat_row=validated_data["seat_row"],
#                 seat_column=validated_data["seat_column"]
#         ).exists():
#             raise ValidationError("seat location is already filled")
#
#         seat = StadiumSeat(**validated_data)
#
#         # add the stadium object passed from view
#         seat.stadium = self.__get_stadium()
#         seat.save()
#         return seat
