from django.http import Http404
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework.response import Response
from datetime import date
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound, ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from organisations.models import Organisation
from utils.exceptionhandler import CustomException
from .models import Product, Category, Inventory
from .service import CategoryService, ProductService
from .serializers import ProductSerializer, CategorySerializer, InventorySerializer


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category
    organisation -- organisation_uid"""

    serializer_class = CategorySerializer
    lookup_field = "category_uid"
    category_service = CategoryService()
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query set for Category view from the request"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                categories = Category.objects.order_by("id")
                return categories
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                categories = Category.objects.filter(organisation=organisation).order_by("id")
                return categories
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

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
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            instance.updated_date = date.today()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Http404:
            raise CustomException(404, "Category not available")
        except ValidationError as exc:
            raise CustomException(400, list(exc.get_full_details().values())[0][0]['message'])

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
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query set for Product view from the request"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                products = Product.objects.order_by("id")
                return products
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                products = Product.objects.filter(organisation=organisation).order_by("id")
                return products
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        try:
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
        except ValidationError as exc:
            raise CustomException(400, list(exc.get_full_details().values())[0][0]['message'])
        except Category.DoesNotExist:
            raise CustomException(404, "Invalid Category")

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
        except Http404:
            raise CustomException(404, "Product not available")
        except ValidationError as exc:
            raise CustomException(400, list(exc.get_full_details().values())[0][0]['message'])

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
                Products"""
        try:
            instance = self.get_object()
            super().perform_destroy(instance)
            return Response({"message": "Product Deleted"})
        except Http404:
            raise CustomException(404, "Object not available")


class CategoryProductView(generics.ListAPIView):
    """Used for Filtering out Products based on the Category given"""

    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("organisation",)
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                products = Product.objects.order_by("id")
                return products
            else:
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


class InventoryView(generics.ListAPIView):
    """Used for Filtering out Products based on the Category given"""

    serializer_class = InventorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("organisation",)
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                inventories = Inventory.objects.order_by("id")
                return inventories
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                inventories = Inventory.objects.filter(organisation=organisation).order_by("id")
                return inventories
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(404, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the products for the Category id given"""

        try:
            product_uid = self.kwargs["product"]
            organisation_id = self.request.query_params.get("organisation", None)
            inventories = Inventory.objects.filter(
                product=product_uid, organisation_id=organisation_id
            )
            serialized = InventorySerializer(inventories, many=True)
            return Response(serialized.data)
        except Inventory.DoesNotExist:
            raise CustomException(404, "The requested category does not exist")
