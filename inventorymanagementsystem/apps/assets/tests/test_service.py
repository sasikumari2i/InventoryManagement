from django.test import TestCase
from unittest import mock
from ..service import AssetService,RepairingStockService
from organisations.models import Organisation
from ..models import Asset, RepairingStock
from ...products.models import Product
from ...orders.models import Invoice

class AssetServiceTest(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        self.organisation_uid = organisation.organisation_uid
        self.asset_service = AssetService()
        # self.vendor_service = VendorService()
        # self.order_service = OrderService()

        self.customer = Customer.objects.create(
            name="Sasi",
            address="Chennai",
            email="sasi@gmail.com",
            phone_number=8789878981,
            organisation_id=self.organisation_uid,
        )

        self.product = Product.objects.create(
            name="Lenovo Thinkpad",
            description="Thinkpad mod_001 i3 8GB RAM GRP",
            category_id=self.category.category_uid,
            organisation_id=self.organisation_uid,
        )

    def test_create_asset(self):
        str_customer = str(self.customer.customer_uid)
        str_product = str(self.product.product_uid)
        payload = {
            "name": "DELL Laptop Sam",
            "serial_no": "ser_no_1",
            "customer": str_customer,
            "product": str_product
        }
        new_asset = self.asset_service.create(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_customer, Asset))
        self.assertEqual(new_asset.name, 'DELL Laptop Sam')


    # def test_create_vendor(self):
    #     payload = {
    #         "name": "Lenovo Vendors Sample",
    #         "address": "Chennai",
    #         "email": "lenovovensam@lenovo.com",
    #         "phone_number": "8789878981"
    #     }
    #     new_vendor = self.vendor_service.create(payload, self.organisation_uid)
    #     self.assertTrue(isinstance(new_vendor, Vendor))
    #     self.assertEqual(new_vendor.name, 'Lenovo Vendors Sample')
    #
    #
    # def test_create_order(self):
    #
    #     str_vendor = str(self.vendor.vendor_uid)
    #     str_product = str(self.product.product_uid)
    #     payload = {
    #         "vendors" : str_vendor,
    #         "delivery_date" : "2022-06-07"
    #     }
    #     order_products = [
    #         {
    #             "product": str_product,
    #             "quantity": 10,
    #             "price": 10000
    #         }
    #     ]
    #     new_order = self.order_service.create(payload,order_products, self.organisation_uid)
    #     self.assertTrue(isinstance(new_order, Order))
    #     invoice = Invoice.objects.get(order_id=new_order.order_uid)
    #     self.assertEqual(invoice.order, new_order)
    #     # print(invoice)
    #     # new_order_product = OrderProduct.objects.get(order=new_order)
    #     # new_product = new_order_product.product
    #     # print(new_product.id)
    #     # print(product.id)
    #     # self.assertEqual(new_product.available_stock, product.available_stock)
    #     # print(new_product.available_stock)
    #     # self.assertEqual(new_order.available_stock, 10)
    #
    # def test_update_order(self):
    #
    #     str_vendor = str(self.vendor.vendor_uid)
    #     str_product = str(self.product.product_uid)
    #
    #     payload = {
    #         "vendors": str_vendor,
    #         "delivery_date": "2022-06-07"
    #     }
    #     order_products = [
    #         {
    #             "product": str_product,
    #             "quantity": 20,
    #             "price": 10000
    #         }
    #     ]
    #
    #     updated_order = self.order_service.update(self.order, payload, order_products, self.organisation_uid)
    #     self.assertTrue(isinstance(updated_order, Order))
    #
    # def test_update_delivery(self):
    #     status_response = self.order_service.update_delivery(self.order)
    #     self.assertEqual(status_response['message'], "Delivery Status Updated")