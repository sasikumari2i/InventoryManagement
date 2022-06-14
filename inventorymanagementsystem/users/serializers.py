# from rest_framework import serializers
# from .models import User
#
#
# class UserSerializer(serializers.ModelSerializer):
#
#     password = serializers.CharField(
#         write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ("id", "name", "email", "phone_number", "is_admin")
#
#     def create(self, validated_data):
#         user = User.objects.create(
#           name=validated_data['name'],
#           email=validated_data['email'],
#           contact_number=validated_data['contact_number'],
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#         application = Application.objects.create(
#             user=user,
#             authorization_grant_type='password',
#             client_type="confidential",
#             name=user.name
#         )
#         application.save()
#         print(application)
#         return user