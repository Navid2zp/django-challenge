from django.db import models


class Stadium(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    row_count = models.PositiveIntegerField(null=False, blank=False, default=1)
    seat_in_row = models.PositiveIntegerField(null=False, blank=False, default=1)

    def create_rows(self):
        rows = []
        for i in range(1, self.row_count + 1):
            rows.append(StadiumSeatRow(stadium=self, row_number=i, seat_count=self.seat_in_row))
        StadiumSeatRow.objects.bulk_create(rows)

    def create_seats(self):
        rows = self.rows.all()
        seats = []
        for row in rows:
            for i in range(1, row.seat_count + 1):
                seats.append(StadiumSeat(stadium=self, row=row, seat_number=i))
        StadiumSeat.objects.bulk_create(seats)

    def __str__(self):
        return f'{self.name}'


def stadium_view_dir_path(instance, filename: str) -> str:
    """
    Separate directories for each stadium.

    :param instance: Stadium instance
    :param filename: str - name of the file
    :return: str - directory/filename.extension
    """

    return f'stadium_{instance.stadium_id}/{filename}'


class StadiumSeatRow(models.Model):
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.CASCADE, related_name="rows")
    row_number = models.PositiveIntegerField(null=False, blank=False, default=1)
    seat_count = models.PositiveIntegerField(null=False, blank=False, default=1)


class StadiumSeat(models.Model):
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.CASCADE, related_name="seats")
    view = models.ImageField(null=True, blank=True, upload_to=stadium_view_dir_path)
    row = models.ForeignKey(StadiumSeatRow, null=False, blank=False, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.PositiveIntegerField(null=False, blank=False, default=1)

    class Meta:
        unique_together = [
            ['row', 'seat_number', 'stadium']  # a seat position is unique
        ]

    def __str__(self):
        return f'{self.stadium.name} - Row: {self.row.row_number} - Number: {self.seat_number}'
