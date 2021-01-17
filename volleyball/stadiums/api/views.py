from rest_framework.generics import ListCreateAPIView

from stadiums.api.serializers import StadiumSerializer
from stadiums.models import Stadium
from volleyball.api.paginations import DefaultLimitOffsetPagination
from volleyball.api.permissions import DefaultCreatePermission


class StadiumAPI(ListCreateAPIView):
    # Class is responsible for both creating a new stadium and listing stadiums
    # Generally, it would be a good idea to separate create/update logic from retrieve/list logic
    # But we don't have any validation or special methods so we combined them for less code
    # We should separate them if our logic became more complex
    # Separating them will help avoid exposing data that shouldn't be or generally easier management of the logics/data
    # Separating them will also help with a better auto api documentation generation

    serializer_class = StadiumSerializer
    permission_classes = [DefaultCreatePermission]
    queryset = Stadium.objects.all()
    pagination_class = DefaultLimitOffsetPagination
