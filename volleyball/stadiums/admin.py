from django.contrib import admin
from .models import Stadium, StadiumSeat, StadiumSeatRow

admin.site.register(Stadium)
admin.site.register(StadiumSeatRow)
admin.site.register(StadiumSeat)
