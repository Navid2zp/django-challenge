from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from matches.models import Match, MatchSeat
from stadiums.api.serializers import StadiumSerializer
from stadiums.models import StadiumSeatRow


class MatchSerializer(ModelSerializer):
    """ Serializer responsible for generating matches list and creating one"""

    stadium = StadiumSerializer()

    class Meta:
        model = Match
        fields = (
            'id', 'stadium', 'team_a', 'team_b', 'start_time', 'stadium'
        )
        read_only_fields = ('id',)


class MatchSeatSerializer(ModelSerializer):
    """ Serializer responsible for generating matches list and creating one"""

    class Meta:
        model = MatchSeat
        fields = (
            'id', 'row', 'seat_number', 'price',
        )


class AddSeatSerializer(Serializer):
    row = IntegerField(required=True, help_text="seat row")
    from_column = IntegerField(required=True, help_text="starting column range")
    to_column = IntegerField(required=True, help_text="ending column range")
    price = IntegerField(required=True, help_text="ticket price")

    def get_match(self) -> Match:
        return self.context.get("match")

    def validate_row(self, value) -> StadiumSeatRow:
        match = self.get_match()
        if match.stadium.row_count < value:
            raise ValidationError("row doesn't exists")

        try:
            return match.stadium.rows.get(row_number=value)
        except:
            raise ValidationError("row doesn't exists")

    def validate_from_column(self, value):
        if self.get_match().stadium.seat_in_row < value:
            raise ValidationError("seat out of range")
        return value

    def validate_to_column(self, value):
        if self.get_match().stadium.seat_in_row < value:
            raise ValidationError("seat out of range")
        return value

    @staticmethod
    def validate_price(value):
        if value < 0:
            raise ValidationError("ticket price must be greater than 0")
        return value

    def create(self, validated_data):
        match = self.get_match()
        seats = []
        for i in range(validated_data["from_column"], validated_data["to_column"] + 1):
            seats.append(MatchSeat(seat_number=i, match=match, row=validated_data["row"]))
        MatchSeat.objects.bulk_create(seats)
        return {"status": "ok", "message": "seats added"}


