from django.db.models import Q
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.api.permissions import SeatReservationPermission
from matches.models import MatchSeat
from django.utils import timezone


class SeatReservationAPI(APIView):
    """
    User requests to buy a seat.
    Seat will be checked and locked if available. then a payment url will be generated for the user to pay.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, SeatReservationPermission)

    @staticmethod
    def _get_expiration_timedelta() -> timezone.timedelta:
        return timezone.timedelta(minutes=10)

    @staticmethod
    def get_payment_url() -> str:
        return ""

    def patch(self, request, *args, **kwargs):
        try:
            MatchSeat.objects.filter(
                Q(Q(locked_for__isnull=True) | Q(lock_expiration__lt=timezone.now()))
                , id=self.kwargs["seat_id"]
            ).update(locked_for=self.request.user, lock_expiration=self._get_expiration_timedelta())
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": "seat not available"})

        return Response(status=status.HTTP_202_ACCEPTED, data={"payment_url": self.get_payment_url()})


class ReservationVerificationAPI(APIView):
    """
    We'll have a token for each payment url that we generate which we linked with the seat
    We'll check the payment token and verify it, Then check if token matches any reservation.
    Finally, we can finalize the reservation and verify the payment with the payment gateway.
    """

    @staticmethod
    def verify_payment():
        """
        Verify the payment with payment gateway.
        Check if token matches reservation token.
        And etc ...
        """

        return True

    def get_reservation(self) -> MatchSeat:
        """
        Find the reservation with provided token
        """
        return MatchSeat.objects.first()

    def patch(self, request, *args, **kwargs):
        if not self.verify_payment():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": "verification failed"})
        self.get_reservation().verify_reservation()
        return Response(status=status.HTTP_202_ACCEPTED, data={"message": "reservation finalized"})
