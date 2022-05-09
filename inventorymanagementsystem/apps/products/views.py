from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from utils.exceptionhandler import CustomException
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category"""

    queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permissions_classes = [permissions.IsAuthenticated]


    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
        Categories"""

        try:
            super().destroy(request)
            return Response({"message" : "Category Deleted"})
        except NotFound:
            raise CustomException(404, "Object not available")


class ProductView(viewsets.ModelViewSet):
    """Gives the view for the Product"""

    queryset = Product.objects.get_queryset().order_by('id')
    serializer_class = ProductSerializer
    # permissions_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                response = super().list(request)
                return response
            else:
                return Response({"message": "Authentication Error"})
        except NotFound:
            raise(404, "Object not available")

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
                Products"""
        try:
            if request.user.is_authenticated:
                instance = self.get_object()
                super().perform_destroy(instance)
                return Response({"message" : "Product Deleted"})
            else:
                return Response({"message": "Authentication Error"})
        except NotFound:
            raise CustomException(404, "Object not available")
