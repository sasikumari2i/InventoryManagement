from django.test import TestCase

from utils.exceptionhandler import CustomException
from ..service import AssetService, RepairingStockService
from organisations.models import Organisation
from ..models import Asset, RepairingStock
from ...products.models import Product, Category
from apps.orders import Customer


class AssetServiceTest(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create(
            name="Ideas2it", description="Ideas2it Organisation"
        )

        self.organisation_uid = organisation.organisation_uid
        self.asset_service = AssetService()
        self.repairing_stock_service = RepairingStockService()

        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products",
            organisation_id=self.organisation_uid,
        )

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
            available_stock=5,
            category_id=self.category.category_uid,
            organisation_id=self.organisation_uid,
        )

        self.asset = Asset.objects.create(
            name="Sample Asset",
            serial_no="ser_no_1",
            customer_id=self.customer.customer_uid,
            organisation_id=self.organisation_uid,
            product_id=self.product.product_uid,
        )

        self.asset_new = Asset.objects.create(
            name="Sample Asset 2",
            serial_no="ser_no_2",
            customer_id=self.customer.customer_uid,
            organisation_id=self.organisation_uid,
            product_id=self.product.product_uid,
        )

        self.repairing_stock = RepairingStock.objects.create(
            serial_no=self.asset.serial_no,
            asset_id=self.asset.asset_uid,
            product_id=self.asset.product_id,
            organisation_id=self.organisation_uid,
        )

    def test_create_asset(self):
        str_customer = str(self.customer.customer_uid)
        str_product = str(self.product.product_uid)
        payload = {
            "name": "DELL Laptop Sam",
            "serial_no": "ser_no_1",
            "customer": str_customer,
            "product": str_product,
        }

        exception_payload = {
            "serial_no": "ser_no_1",
            "customer": str_customer,
            "product": str_product,
        }
        new_asset = self.asset_service.create(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_asset, Asset))
        self.assertEqual(new_asset.name, "DELL Laptop Sam")

        with self.assertRaises(CustomException):
            self.asset_service.create(exception_payload, self.organisation_uid)

    def test_update_asset(self):
        str_customer = str(self.customer.customer_uid)
        str_product = str(self.product.product_uid)

        payload = {"customer": str_customer, "product": str_product}
        exception_payload = {"customer": str_customer, "product": str_product}
        updated_asset = self.asset_service.update(self.asset, payload)
        self.assertTrue(isinstance(updated_asset, Asset))

        with self.assertRaises(CustomException):
            self.asset_service.create(exception_payload, self.organisation_uid)

    def test_close_asset(self):
        data = {}
        status_response = self.asset_service.close_asset(self.asset, data)
        self.assertEqual(status_response["message"], "Assigned asset is closed")
        updated_status = self.asset_service.close_asset(self.asset, data)
        self.assertEqual(updated_status["message"], "It is already not active")

    def test_create_repairing_stock(self):
        self.asset_new.is_active = False
        self.asset_new.save()
        str_asset = str(self.asset_new.asset_uid)
        payload = {"asset": str_asset}
        exception_payload = {"asset": "98uhgfvb6567656yhgfdrtyugfdsrtyu"}
        new_repairing_stock = self.repairing_stock_service.create(
            payload, self.organisation_uid
        )
        self.assertTrue(isinstance(new_repairing_stock, RepairingStock))

        with self.assertRaises(CustomException):
            self.asset_service.create(exception_payload, self.organisation_uid)

    def test_update_repairing_stock(self):
        str_asset = str(self.asset.asset_uid)
        str_product = str(self.product.product_uid)

        payload = {"asset": str_asset, "product": str_product}
        exception_payload = {"asset": str_asset, "product": str_product}
        updated_repairing_stock = self.repairing_stock_service.update(
            self.repairing_stock, payload
        )
        self.assertTrue(isinstance(updated_repairing_stock, RepairingStock))

        with self.assertRaises(CustomException):
            self.asset_service.create(exception_payload, self.organisation_uid)

    def test_close_repairing_stock(self):
        data = {}
        status_response = self.repairing_stock_service.close_repairing_stock(
            self.repairing_stock, data
        )
        self.assertEqual(status_response["message"], "Repairing Stock asset is closed")
        updated_status = self.repairing_stock_service.close_repairing_stock(
            self.repairing_stock, data
        )
        self.assertEqual(updated_status["message"], "It is already not active")
