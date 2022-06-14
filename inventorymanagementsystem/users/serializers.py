from django.contrib.auth.password_validation import validate_password
from oauth2_provider.models import Application
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_no", "password",
                  "is_active", "is_staff", "is_admin",
                  "created_by", "user_role")

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name
        )
        application.save()
        return user
