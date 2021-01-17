from rest_framework.generics import ListCreateAPIView, get_object_or_404

from stadiums.api.paginations import StadiumLimitOffsetPagination
from stadiums.api.permission import StadiumCreatePermission
from stadiums.api.serializers import StadiumSerializer
from stadiums.models import Stadium, StadiumSeat


class StadiumAPI(ListCreateAPIView):
    # Class is responsible for both creating a new stadium and listing stadiums
    # Generally, it would be a good idea to separate create/update logic from retrieve/list logic
    # But we don't have any validation or special methods so we combined them for less code
    # We should separate them if our logic became more complex
    # Separating them will help avoid exposing data that shouldn't be or generally easier management of the logics/data
    # Separating them will also help with a better auto api documentation generation

    serializer_class = StadiumSerializer
    permission_classes = [StadiumCreatePermission]
    queryset = Stadium.objects.all()
    pagination_class = StadiumLimitOffsetPagination


# class StadiumSeatsAPI(ListCreateAPIView):
#     serializer_class = StadiumSeatSerializer
#     permission_classes = [StadiumCreatePermission]
#     pagination_class = StadiumLimitOffsetPagination
#
#     def get_stadium_id(self):
#         return self.kwargs.get("stadium_id", 0)
#
#     def get_object(self):
#         # in case drf-yasg tried to get the schema
#         if getattr(self, 'swagger_fake_view', False):
#             # queryset just for schema generation metadata
#             return Stadium.objects.none()
#
#         return get_object_or_404(Stadium, id=self.get_stadium_id())
#
#     def get_queryset(self, *args, **kwargs):
#         return StadiumSeat.objects.filter(stadium=self.get_object())
#
#     def get_serializer_context(self):
#         """
#         Pass stadium object to serializer so we can access it there
#         :return: dict - serializer context data
#         """
#
#         return {"request": self.request, "stadium": self.get_object()}
