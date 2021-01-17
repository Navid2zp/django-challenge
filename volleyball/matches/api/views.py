from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from matches.api.serializers import MatchSerializer, AddSeatSerializer, MatchSeatSerializer
from matches.models import Match, MatchSeat
from volleyball.api.paginations import DefaultLimitOffsetPagination
from volleyball.api.permissions import DefaultCreatePermission


class MatchAPI(ListCreateAPIView):
    """
    API responsible for both creating a match and listing the matches.

    GET:
        - Returns a list of all matches
    POST:
        - Creates a new match
    """

    serializer_class = MatchSerializer
    permission_classes = [DefaultCreatePermission]
    queryset = Match.objects.all()
    pagination_class = DefaultLimitOffsetPagination


class MatchSeatsAPI(ListAPIView):
    """
    List of all the matches (state not included).
    Further filtering and options could be added by overriding the get_queryset method.
    This method can be and should be fully cached since there is no state available on the result set.
    This method should only be used to get the details for the available seats and not seats update/states.
    """

    serializer_class = MatchSeatSerializer
    pagination_class = DefaultLimitOffsetPagination

    def get_queryset(self):
        return MatchSeat.objects.filter(match_id=self.kwargs["match_id"])


class MatchAvailableSeatsAPI(APIView):
    """
    Returns a flat list of all the seats that are available (only ids). Example: [1, 2, 6, 45, 61]
    This endpoint should be called to get updates instead of calling the seats endpoint again and again.
    Using a websocket to notify changes will be better idea but this method is fast enough for updating the frontend.
    """

    def get(self, request, match_id, *args, **kwargs):
        seats = MatchSeat.objects.filter(
            Q(Q(locked_for__isnull=True) | Q(lock_expiration__lt=timezone.now())),
            match_id=match_id,
            owner__isnull=True,
        ).values_list("id", flat=True)
        return Response(data=list(seats))


class MatchAddSeatAPI(APIView):
    """
    Generates bulk seats based on the given range in the given row of the stadium.
    """
    permission_classes = [DefaultCreatePermission]
    serializer_class = AddSeatSerializer

    def _get_match(self):
        """
        Find the match or raise HTTP404
        """
        return get_object_or_404(Match, id=self.kwargs.get("match_id"))

    def get_serializer_context(self):
        """
        Add match object to the serializer context so we can use it for validations.
        """
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

        # Allow serializer to raise exception so we won't have to handle them here.
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
