from rest_framework.serializers import ModelSerializer

from stadiums.models import Stadium


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
        return stadium
