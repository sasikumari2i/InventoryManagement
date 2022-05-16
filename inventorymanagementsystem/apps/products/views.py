from rest_framework.response import Response
from rest_framework.request import Request
from datetime import date, timedelta
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import permissions, authentication

from organisations.models import Organisation
from utils.exceptionhandler import CustomException
from .models import Product, Category
from .service import CategoryService, ProductService
from .serializers import ProductSerializer, CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category"""

    # queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer
    category_service = CategoryService()

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation',None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            categories = Category.objects.filter(organisation=organisation).order_by('id')
            return categories
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        validated_data = CategorySerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        organisation = self.request.query_params.get('organisation', None)
        new_category = self.category_service.create(validated_data, organisation)
        serialized = CategorySerializer(new_category)
        return Response(serialized.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.updated_date = date.today()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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

    # queryset = Product.objects.get_queryset().order_by('id')
    serializer_class = ProductSerializer
    product_service = ProductService()

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            products = Product.objects.filter(organisation=organisation).order_by('id')
            return products
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        validated_data = ProductSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        organisation = self.request.query_params.get('organisation', None)
        new_product = self.product_service.create(validated_data, organisation)
        serialized = ProductSerializer(new_product)
        return Response(serialized.data)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            category = Category.objects.filter(id=request.data['category'],
                                            organisation_id=instance.organisation)
            instance.updated_date = date.today()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise CustomException(404, "Invalid Category")




    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
                Products"""
        try:
            instance = self.get_object()
            super().perform_destroy(instance)
            return Response({"message" : "Product Deleted"})
        except NotFound:
            raise CustomException(404, "Object not available")


class CategoryProductView(generics.ListAPIView):

    # queryset = Payment.objects.get_queryset().order_by('id')
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            products = Product.objects.filter(organisation=organisation).order_by('id')
            return products
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")


    def get(self, request, *args, **kwargs):
        """Retrieves the payments for the Invoice id given"""

        try:
            category_id = self.kwargs['category']
            organisation_id = self.request.query_params.get('organisation', None)
            products = Product.objects.filter(category=category_id,organisation_id=organisation_id)
            serialized = ProductSerializer(products, many=True)
            return Response(serialized.data)
        except Product.DoesNotExist:
            raise CustomException(404, "The requested category does not exist")

