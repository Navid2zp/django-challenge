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
