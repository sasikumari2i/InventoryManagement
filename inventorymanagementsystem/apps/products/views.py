from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from utils.exceptionhandler import CustomException
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category"""

    queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
        Categories"""

        try:
            super().destroy(request)
            return Response({"message" : "Category Deleted"})
        except ObjectDoesNotExist:
            raise CustomException(404, "Object not available")


class ProductView(viewsets.ModelViewSet):
    """Gives the view for the Product"""

    queryset = Product.objects.get_queryset().order_by('id')
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
                Products"""
        try:
            super().destroy(request)
            return Response({"message" : "Product Deleted"})
        except NotFound:
            raise CustomException(404, "Object not available")

