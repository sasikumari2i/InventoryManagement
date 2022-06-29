# from django.core.exceptions import ValidationError
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import logging

from organisations.models import Organisation
from .models import Invoice, Payment
from .service import InvoiceService, PaymentService
from .serializers import InvoiceSerializer, PaymentSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger("django")


class InvoiceView(viewsets.ViewSet):
    """Gives the view for the Invoice"""

    serializer_class = InvoiceSerializer
    invoice_service = InvoiceService()
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query Set for the getting Invoices"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                invoices = Invoice.objects.order_by("id")
                return invoices
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                invoices = Invoice.objects.filter(organisation=organisation).order_by("id")
                return invoices
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new invoice, overrided from ModelViewSet class"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            order_id = request.data["order"]
            validated_data = InvoiceSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_invoice = self.invoice_service.create(
                validated_data.data, order_id, organisation
            )
            serialized = InvoiceSerializer(new_invoice)
            return Response(serialized.data)
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)

    def retrieve(self, request, pk):
        """Retrieve the invoice using the given Id"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            invoice = self.invoice_service.retrieve(pk, organisation)
            serialized = InvoiceSerializer(invoice)
            return Response(serialized.data)
        except Invoice.DoesNotExist:
            raise CustomException(404, "Invoice Not Found")

    def list(self, request):
        """List all the invoices of the organisation"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            invoice = Invoice.objects.filter(organisation_id=organisation)
            serialized = InvoiceSerializer(invoice, many=True)
            return Response(serialized.data)
        except Invoice.DoesNotExist:
            raise CustomException(404, "Invoice Not Found")

    def destroy(self, request, pk):
        """Soft Delete the invoice Id given"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            invoice = Invoice.objects.get(invoice_uid=pk, organisation_id=organisation)
            invoice.delete()
            return Response({"message": "Invoice Deleted"})
        except Invoice.DoesNotExist:
            raise CustomException(404, "Invoice Not Found")


class PaymentView(viewsets.ModelViewSet):
    """Gives the view for the Payment"""

    serializer_class = PaymentSerializer
    lookup_field = "payment_uid"
    payment_service = PaymentService()
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query Set for the getting Payments"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                payments = Payment.objects.order_by("id")
                return payments
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                payments = Payment.objects.filter(organisation=organisation).order_by("id")
                return payments
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new payment, overrided from ModelViewSet class"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            invoice_uid = request.data["invoice"]
            validated_data = PaymentSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_payment = self.payment_service.create(
                validated_data.data, invoice_uid, organisation
            )
            serialized = PaymentSerializer(new_payment)
            return Response(serialized.data)
        except CustomException as exc:
            logger.error("Custom Exception in Payment Creation")
            raise CustomException(exc.status_code, exc.detail)
        except ValidationError:
            raise CustomException(400, "Enter a valid name")

    def update(self, request, *args, **kwargs):
        """Overided Update method for restricting the updates"""

        return Response({"message": "Payment cannot be updated"})


class InvoicePaymentView(generics.ListAPIView):
    """Gives the view for the Payment using the invoice given"""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query Set for the getting Payments"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                payments = Payment.objects.order_by("id")
                return payments
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                payments = Payment.objects.filter(organisation=organisation).order_by("id")
                return payments
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the payments for the Invoice id given"""

        try:
            invoice_id = self.kwargs["invoice"]
            payment = Payment.objects.filter(invoice=invoice_id)
            serialized = PaymentSerializer(payment, many=True)
            return Response(serialized.data)
        except Payment.DoesNotExist:
            raise CustomException(404, "The requested invoice does not exist")


class InvoiceStatusView(generics.GenericAPIView):
    """Gives the view for the Invoice to update the payment status"""

    serializer_class = InvoiceSerializer
    lookup_field = "invoice_uid"
    invoice_service = InvoiceService()
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['staff']

    def get_queryset(self):
        """Query Set for the getting Invoices"""

        try:
            organisation_uid = self.request.user.organisation_id
            if organisation_uid is None and self.request.user.user_role == "staff":
                raise CustomException(400, "Credentials required")
            elif self.request.user.user_role == "super_user":
                invoices = Invoice.objects.order_by("id")
                return invoices
            else:
                organisation = Organisation.objects.get(organisation_uid=organisation_uid)
                invoices = Invoice.objects.filter(organisation=organisation).order_by("id")
                return invoices
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        """Updates the payment status for the Invoice given"""

        try:
            invoice_details = self.get_object()
            response = self.invoice_service.update_invoice(invoice_details)
            return Response(response)
        except Invoice.DoesNotExist:
            raise CustomException(404, "Exception in Updating Invoice Status")
