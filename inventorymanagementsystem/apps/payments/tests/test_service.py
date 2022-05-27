from django.test import TestCase
from unittest import mock
from ..service import InvoiceService, PaymentService
from organisations.models import Organisation
from ..models import Payment,Invoice
from ...orders.models import Vendor, Customer, OrderProduct, Order
from ...products.models import Product, Category


class PaymentServiceTest(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(
            name="Ideas2it", description="Ideas2it Organisation"
        )

        self.organisation_uid = organisation.organisation_uid
        self.invoice_service = InvoiceService()
        self.payment_service = PaymentService()

        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products",
            organisation_id=self.organisation_uid,
        )

        self.product = Product.objects.create(
            name="Lenovo Thinkpad",
            description="Thinkpad mod_001 i3 8GB RAM GRP",
            category_id=self.category.category_uid,
            organisation_id=self.organisation_uid,
        )

        self.vendor = Vendor.objects.create(
            name="Lenovo Vendors Sample",
            address="Chennai",
            email="lenovovensam@lenovo.com",
            phone_number=8789878981,
            organisation_id=self.organisation_uid,
        )

        str_vendor_uid = str(self.vendor.vendor_uid)

        self.order = Order.objects.create(
            delivery_date="2022-06-03",
            vendors_id=str_vendor_uid,
            organisation_id=self.organisation_uid,
        )

        self.order_product = OrderProduct.objects.create(
            product=self.product, order=self.order, quantity=10
        )


    def test_create_invoice(self):
        str_order = str(self.order.order_uid)

        payload = {
            "order": str_order,
            "payment_deadline" : "2022-06-03"
        }
        new_invoice = self.invoice_service.create(payload, str_order, self.organisation_uid)
        self.assertTrue(isinstance(new_invoice, Invoice))

    def test_update_invoice(self):

        invoice = Invoice.objects.create(
            amount=0,
            order=self.order,
            organisation_id=self.organisation_uid,
        )
        updated_invoice = self.invoice_service.update_invoice(invoice)
        self.assertEqual(updated_invoice, "Invoice Status Updated")
        print(updated_invoice)