from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_no", "password",
                  "is_active", "is_staff", "is_admin",
                  "created_by", "user_role", "organisation")


