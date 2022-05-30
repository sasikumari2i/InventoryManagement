from django.test import TestCase
from ..service import CategoryService, ProductService
from organisations.models import Organisation
from ..models import Category, Product
from utils.exceptionhandler import CustomException


class ProductServiceTest(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create(
            name="Ideas2it", description="Ideas2it Organisation"
        )

        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products",
            organisation_id=organisation.organisation_uid,
        )

        self.organisation_uid = organisation.organisation_uid
        self.category_service = CategoryService()
        self.product_service = ProductService()

    def test_create_category(self):
        payload = {"name": "Electronics", "description": "Electronic products"}
        new_category = self.category_service.create_category(
            payload, self.organisation_uid
        )
        exception_payload = {"description": "Electronic products"}

        self.assertTrue(isinstance(new_category, Category))
        self.assertEqual(new_category.name, "Electronics")

        with self.assertRaises(CustomException):
            self.category_service.create_category(
                exception_payload, self.organisation_uid
            )

    def test_create_product(self):
        str_category = str(self.category.category_uid)
        payload = {
            "name": "Lenovo Thinkpad",
            "description": "Thinkpad mod_001 i3 8GB RAM GRP",
            "category": str_category,
        }

        category = Category.objects.get(
            organisation_id=self.organisation_uid, category_uid=str_category,
        )

        exception_payload = {
            "description": "Thinkpad mod_001 i3 8GB RAM GRP",
            "category": str_category,
        }

        exception_payload_category = {
            "name": "Lenovo Thinkpad",
            "description": "Thinkpad mod_001 i3 8GB RAM GRP",
            "category": "str_category",
        }

        with self.assertRaises(CustomException):
            self.product_service.create_product(
                exception_payload, self.organisation_uid
            )

        with self.assertRaises(CustomException):
            self.product_service.create_product(
                exception_payload_category, self.organisation_uid
            )

        self.assertTrue(isinstance(category, Category))
        new_product = self.product_service.create_product(
            payload, self.organisation_uid
        )
        self.assertTrue(isinstance(new_product, Product))
        self.assertEqual(new_product.name, "Lenovo Thinkpad")
