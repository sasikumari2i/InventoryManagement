from rest_framework.response import Response
from rest_framework.request import Request
from datetime import date, timedelta
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import permissions, authentication
from django_filters.rest_framework import DjangoFilterBackend

from organisations.models import Organisation
from utils.exceptionhandler import CustomException
from .models import Product, Category
from .service import CategoryService, ProductService
from .serializers import ProductSerializer, CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category
    organisation -- organisation_uid"""

    serializer_class = CategorySerializer
    lookup_field = "category_uid"
    category_service = CategoryService()

    def get_queryset(self):
        """Query set for Category view from the request"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            categories = Category.objects.filter(organisation_id=organisation).order_by(
                "id"
            )
            return categories
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    # def list(self, request, *args, **kwargs):
    #
    #     response = super().list(request)
    #     return response

    def create(self, request, *args, **kwargs):

        try:
            validated_data = CategorySerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            organisation_uid = self.request.query_params.get("organisation")
            if organisation_uid is None:
                raise CustomException(404, "Credentials Required")
            new_category = self.category_service.create_category(
                validated_data.data, organisation_uid
            )
            serialized = CategorySerializer(new_category)
            return Response(serialized.data)
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
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
            return Response({"message": "Category Deleted"})
        except NotFound:
            raise CustomException(404, "Object not available")


class ProductView(viewsets.ModelViewSet):
    """Gives the view for the Product"""

    serializer_class = ProductSerializer
    lookup_field = "product_uid"
    product_service = ProductService()

    def get_queryset(self):
        """Query set for Product view from the request"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            products = Product.objects.filter(organisation=organisation).order_by("id")
            return products
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        validated_data = ProductSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        organisation_uid = self.request.query_params.get("organisation", None)
        if organisation_uid is None:
            raise CustomException(404, "Credentials Required")
        new_product = self.product_service.create_product(
            validated_data.data, organisation_uid
        )
        serialized = ProductSerializer(new_product)
        return Response(serialized.data)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", True)
            instance = self.get_object()
            instance.updated_date = date.today()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            response = self.perform_update(serializer)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise CustomException(404, "Invalid Category")

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
                Products"""
        try:
            instance = self.get_object()
            super().perform_destroy(instance)
            return Response({"message": "Product Deleted"})
        except NotFound:
            raise CustomException(404, "Object not available")


class CategoryProductView(generics.ListAPIView):
    """Used for Filtering out Products based on the Category given"""

    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("organisation",)

    def get_queryset(self):
        try:
            if self.request.query_params is None:
                raise CustomException(400, "Credentials required")
            # if organisation_uid is None:
            #     raise CustomException(400, "Credentials required")
            organisation_uid = self.request.query_params.get("organisation")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            products = Product.objects.filter(organisation=organisation).order_by("id")
            return products
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the products for the Category id given"""

        try:
            category_uid = self.kwargs["category"]
            organisation_id = self.request.query_params.get("organisation", None)
            products = Product.objects.filter(
                category=category_uid, organisation_id=organisation_id
            )
            serialized = ProductSerializer(products, many=True)
            return Response(serialized.data)
        except Product.DoesNotExist:
            raise CustomException(404, "The requested category does not exist")
