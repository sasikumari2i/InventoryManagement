from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True)

    class Meta:
        model = User
        fields = ("user_uid", "name", "email", "phone_no", "password",
                  "is_active", "is_admin",
                  "created_by", "organisation")


