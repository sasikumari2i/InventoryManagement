from rest_framework import serializers
from .models import Csv, Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ("organisation_uid", "name", "description")

class CSVUploadSerializer(serializers.ModelSerializer):

    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Csv
        fields = '__all__'
