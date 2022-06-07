from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from utils.exceptionhandler import CustomException
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated


class OrganisationView(viewsets.ModelViewSet):
    """Organisation level view class for CRUD operations"""

    queryset = Organisation.objects.order_by("id")
    lookup_field = "organisation_uid"
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request, *args, **kwargs):
        print(request.meta.USERNAME)

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
        Categories"""

        try:
            super().destroy(request)
            return Response({"message": "Organisation Deleted"})
        except Http404:
            raise CustomException(404, "Object not available")