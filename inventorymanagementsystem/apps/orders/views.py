from rest_framework.response import Response
from rest_framework import viewsets, generics
import logging
from datetime import date
from rest_framework.exceptions import NotFound, ValidationError
from django.http import Http404

from organisations.models import Organisation
from .models import Order, Customer, Vendor
from .service import OrderService, VendorService, CustomerService
from .serializers import (
    CustomerSerializer,
    VendorSerializer,
    DeliverySerializer,
    OrderSerializer,
)
from utils.exceptionhandler import CustomException

logger = logging.getLogger("django")


class OrderView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    serializer_class = OrderSerializer
    lookup_field = "order_uid"
    order_service = OrderService()

    def get_queryset(self):
        """Query Set for the getting Orders"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            orders = Order.objects.filter(organisation=organisation).order_by("id")
            return orders
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def retrieve(self, request, *args, **kwargs):
        """Retrieves specific order for the given order id"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound as exc:
            raise CustomException(exc.status_code, "Exception in Retrieving Orders")
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)

    def create(self, request, *args, **kwargs):
        """Creates new order using given data"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            order_products = request.data["order_products"]
            # request.data.pop("order_products")
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_order = self.order_service.create(
                validated_data.data, order_products, organisation_uid
            )
            serialized = OrderSerializer(new_order)
            return Response(serialized.data)
        except Vendor.DoesNotExist:
            raise CustomException(400, "KeyError in Order Creation View")

    def update(self, request, *args, **kwargs):
        """Updates the given order"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            order_details = self.get_object()
            # if order_details.delivery_status:
            #     raise CustomException(400, "Delivered product cannot be updated")
            order_products = request.data["order_products"]
            request.data.pop("order_products")
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            order = self.order_service.update(
                order_details, validated_data.data, order_products, organisation_uid
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except KeyError:
            raise CustomException(400, "Provide all the required credentials")
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)

    def partial_update(self, request, *args, **kwargs):
        """Updates partial fields for the given order"""

        try:
            response = self.update(request)
            return response
        except KeyError:
            raise CustomException(400, "Provide all the required credentials")

    def destroy(self, request, *args, **kwargs):
        """Deletes the given order"""

        try:
            super().destroy(request)
            return Response({"message": "Order Deleted"})
        except Http404:
            raise CustomException(404, "Exception in Delete Order")
        except CustomException as exc:
            raise CustomException(exc.status_code,exc.detail)


class CustomerView(viewsets.ModelViewSet):
    """Gives the view for the Customer"""

    serializer_class = CustomerSerializer
    lookup_field = "customer_uid"
    customer_service = CustomerService()

    def get_queryset(self):
        """Query Set for the getting Customers"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            customers = Customer.objects.filter(organisation=organisation).order_by(
                "id"
            )
            return customers
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new customer using given data"""

        try:
            validated_data = CustomerSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            organisation = self.request.query_params.get("organisation", None)
            new_customer = self.customer_service.create(
                validated_data.data, organisation
            )
            serialized = CustomerSerializer(new_customer)
            return Response(serialized.data)
        except ValidationError as exc:
            raise CustomException(404, list(exc.get_full_details().values())[0][0]['message'])

    def update(self, request, *args, **kwargs):
        """Updates customer using given data"""

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            instance.updated_date = date.today()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as exc:
            raise CustomException(404, list(exc.get_full_details().values())[0][0]['message'])

    def destroy(self, request, *args, **kwargs):
        """Deletes the given customer"""

        try:
            super().destroy(request)
            return Response({"message": "Customer Deleted"})
        except Http404:
            raise CustomException(404, "Customer not found")


class VendorView(viewsets.ModelViewSet):
    """Gives the view for the Vendor"""

    serializer_class = VendorSerializer
    lookup_field = "vendor_uid"
    vendor_service = VendorService()

    def get_queryset(self):
        """Query Set for the getting Vendors"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            vendors = Vendor.objects.filter(organisation=organisation).order_by("id")
            return vendors
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new Vendor using given data"""

        try:
            validated_data = VendorSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            organisation = self.request.query_params.get("organisation", None)
            new_vendor = self.vendor_service.create(validated_data.data, organisation)
            serialized = VendorSerializer(new_vendor)
            return Response(serialized.data)
        except ValidationError as exc:
            raise CustomException(404, list(exc.get_full_details().values())[0][0]['message'])

    def update(self, request, *args, **kwargs):
        """Updates vendor using given data"""

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            instance.updated_date = date.today()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError:
            raise CustomException(400, "Exception in vendor updation")

    def destroy(self, request, *args, **kwargs):
        """Deletes the given vendor"""

        try:
            super().destroy(request)
            return Response({"message": "Vendor Deleted"})
        except Http404:
            raise CustomException(404, "Vendor not found")


class DeliveryView(generics.GenericAPIView):
    """Gives the view for updating delivery status of order"""

    # serializer_class = DeliverySerializer
    lookup_field = "order_uid"
    order_service = OrderService()

    def get_queryset(self):
        """Query Set for the getting Orders"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            orders = Order.objects.filter(organisation=organisation).order_by("id")
            return orders
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        """Updates the delivery status of the order"""

        try:
            order_details = self.get_object()
            response = self.order_service.update_delivery(order_details)
            return Response(response)
        except Http404:
            raise CustomException(404, "Exception in Updating Delivery Status")


class VendorOrderView(generics.ListAPIView):
    """Gives the view for retrieving orders for the given vendor"""

    serializer_class = OrderSerializer
    lookup_field = "vendors"

    def get_queryset(self):
        """Query Set for the getting Vendors"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            orders = Order.objects.filter(organisation=organisation).order_by("id")
            return orders
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        try:
            vendor_id = self.kwargs["vendors"]
            orders = Order.objects.filter(vendors=vendor_id)
            serialized = OrderSerializer(orders, many=True)
            return Response(serialized.data)
        except NotFound:
            raise CustomException(
                404, "Requested Orders for the Vendor is not available"
            )
