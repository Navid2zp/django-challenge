from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from matches.api.serializers import MatchSerializer, AddSeatSerializer
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
    permission_classes = [DefaultCreatePermission]
    queryset = Match.objects.all()
    pagination_class = DefaultLimitOffsetPagination


# class MatchDetailAPI(RetrieveAPIView):
#
#     serializer_class = MatchDetailSerializer
#     queryset = Match.objects.all()
#     pagination_class = DefaultLimitOffsetPagination
#
#     lookup_field = 'id'
#     lookup_url_kwarg = 'match_id'


class MatchAddSeatAPI(APIView):
    permission_classes = [DefaultCreatePermission]
    serializer_class = AddSeatSerializer

    def _get_match(self):
        return get_object_or_404(Match, id=self.kwargs.get("match_id"))

    def get_serializer_context(self):
        return {"request": self.request, "match": self._get_match()}

    @swagger_auto_schema(query_serializer=AddSeatSerializer())
    def post(self, request, match_id):
        """
        Each row has a number of seats. You can provide a range for the seats to be added.
        For example:
         {
            "row": 1,
            "from_column": 1,
            "to_column": 5,
            "price": 5000
         }
         Will add 5 seats in row number 1 with seat numbers 1 to 5
        """
        serializer = AddSeatSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

