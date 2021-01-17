from rest_framework.pagination import LimitOffsetPagination


class StadiumLimitOffsetPagination(LimitOffsetPagination):
    """
    Default pagination class for stadium endpoints
    """
    default_limit = 50  # default number items
    max_limit = 200  # max number of items allowed
