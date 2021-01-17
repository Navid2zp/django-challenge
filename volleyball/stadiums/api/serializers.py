from rest_framework.serializers import ModelSerializer

from stadiums.models import Stadium


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
