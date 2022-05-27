from django.test import TestCase
from unittest import mock
from ..service import CustomerService, VendorService, OrderService
from ..serializers import CustomerSerializer, VendorSerializer
from organisations.models import Organisation
from ..models import Customer, Vendor, Order, OrderProduct
from ...products.models import Product, Category
from ...payments.models import Invoice


class OrderServiceTest(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create(
            name="Ideas2it", description="Ideas2it Organisation"
        )

        self.organisation_uid = organisation.organisation_uid
        self.customer_service = CustomerService()
        self.vendor_service = VendorService()
        self.order_service = OrderService()

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

    def test_create_customer(self):
        payload = {
            "name": "Sasi",
            "address": "Chennai",
            "email": "sasi@gmail.com",
            "phone_number": "8789878916",
        }
        new_customer = self.customer_service.create(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_customer, Customer))
        self.assertEqual(new_customer.name, "Sasi")

    def test_create_vendor(self):
        payload = {
            "name": "Lenovo Vendors Sample",
            "address": "Chennai",
            "email": "lenovovensam@lenovo.com",
            "phone_number": "8789878981",
        }
        new_vendor = self.vendor_service.create(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_vendor, Vendor))
        self.assertEqual(new_vendor.name, "Lenovo Vendors Sample")

    def test_create_order(self):

        str_vendor = str(self.vendor.vendor_uid)
        str_product = str(self.product.product_uid)
        payload = {"vendors": str_vendor, "delivery_date": "2022-06-07"}
        order_products = [{"product": str_product, "quantity": 10, "price": 10000}]
        new_order = self.order_service.create(
            payload, order_products, self.organisation_uid
        )
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.available_stock, 10)
        self.assertTrue(isinstance(new_order, Order))
        invoice = Invoice.objects.get(order_id=new_order.order_uid)
        self.assertEqual(invoice.order, new_order)
        # print(invoice)
        # new_order_product = OrderProduct.objects.get(order=new_order)
        # new_product = new_order_product.product
        # print(new_product.available_stock)
        # print(new_product.id)
        # print(self.product.id)
        # print(product.id)
        # self.assertEqual(new_product.available_stock, product.available_stock)
        # print(new_product.available_stock)
        # self.assertEqual(new_order.available_stock, 10)

    def test_update_order(self):

        str_vendor = str(self.vendor.vendor_uid)
        str_product = str(self.product.product_uid)

        payload = {"vendors": str_vendor, "delivery_date": "2022-06-07"}
        order_products = [{"product": str_product, "quantity": 20, "price": 10000}]

        updated_order = self.order_service.update(
            self.order, payload, order_products, self.organisation_uid
        )
        self.assertTrue(isinstance(updated_order, Order))

    def test_update_delivery(self):
        status_response = self.order_service.update_delivery(self.order)
        self.assertEqual(status_response["message"], "Delivery Status Updated")
