from rest_framework import viewsets

from .models import Organisation
from .serializers import OrganisationSerializer


# Create your views here.
class OrganisationView(viewsets.ModelViewSet):
    """Organisation level view class for CRUD operations"""

    queryset = Organisation.objects.order_by("id")
    lookup_field = "organisation_uid"
    serializer_class = OrganisationSerializer
