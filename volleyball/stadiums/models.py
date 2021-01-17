from django.db import models


class Stadium(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    capacity = models.PositiveIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f'{self.name} - Capacity: {self.capacity}'


def stadium_view_dir_path(instance: Stadium, filename: str) -> str:
    """
    Separate directories for each stadium.

    :param instance: Stadium instance
    :param filename: str - name of the file
    :return: str - directory/filename.extension
    """

    return f'stadium_{instance.id}/{filename}'


class StadiumSeat(models.Model):
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.CASCADE, related_name="seats")
    seat_code = models.PositiveIntegerField(null=False, blank=False)
    view = models.ImageField(null=True, blank=True, upload_to=stadium_view_dir_path)

    class Meta:
        unique_together = ('stadium', 'seat_code',)  # a stadium can't have more than one seat with the same code
