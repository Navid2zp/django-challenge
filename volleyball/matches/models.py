from django.db import models

from stadiums.models import Stadium, StadiumSeatRow


class Match(models.Model):
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.PROTECT, related_name="matches")

    # Teams should have their own model but we're just going to use a simple CharField here because of time limits
    team_a = models.CharField(null=False, blank=False, max_length=80)
    team_b = models.CharField(null=False, blank=False, max_length=80)

    start_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.team_a} vs {self.team_b}'


class MatchSeat(models.Model):
    match = models.ForeignKey(Match, null=False, blank=False, on_delete=models.CASCADE, related_name="seats")
    row = models.ForeignKey(StadiumSeatRow, null=False, blank=False, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField(null=False, blank=False, default=1)
    price = models.PositiveIntegerField(null=False, blank=False, default=1000)

    class Meta:
        unique_together = [
            ['row', 'seat_number', 'match']  # a seat position is unique
        ]

    def __str__(self):
        return f'{self.match.team_a} vs {self.match.team_b} - Row: {self.row.row_number} - Number: {self.seat_number}'
