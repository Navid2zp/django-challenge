from rest_framework.serializers import ModelSerializer

from matches.models import Match


class MatchSerializer(ModelSerializer):
    """ Serializer responsible for generating matches list and creating one"""

    class Meta:
        model = Match
        fields = (
            'id', 'stadium', 'team_a', 'team_b', 'start_time'
        )
        read_only_fields = ('id',)
