from rest_framework import permissions
from datetime import datetime


class SeatReservationPermission(permissions.BasePermission):
    message = 'Seat is not available.'

    def has_object_permission(self, request, view, obj):
        """
        Only allow a seat to be reservable if it's not already reserved or payment is expired
        """
        if not obj.locked_for or obj.lock_expiration < datetime.now():
            return True
        return False
