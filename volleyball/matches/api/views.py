from rest_framework.generics import ListCreateAPIView

from matches.api.serializers import MatchSerializer
from matches.models import Match
from volleyball.api.paginations import DefaultLimitOffsetPagination
from volleyball.api.permissions import DefaultCreatePermission


class MatchAPI(ListCreateAPIView):
    """
    GET:
        - Returns a list of all matches
    POST:
        - Creates a new match
    """

    serializer_class = MatchSerializer
    permission_classes = [DefaultLimitOffsetPagination]
    queryset = Match.objects.all()
    pagination_class = DefaultCreatePermission

