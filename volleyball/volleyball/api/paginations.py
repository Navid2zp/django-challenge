from rest_framework.pagination import LimitOffsetPagination


class DefaultLimitOffsetPagination(LimitOffsetPagination):
    """
    Default pagination class
    """
    default_limit = 50  # default number items
    max_limit = 200  # max number of items allowed
