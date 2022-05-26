from django.test import TestCase
from unittest import mock
from ..service import CategoryService, ProductService
from ..serializers import CategorySerializer, ProductSerializer
from organisations.models import Organisation
from ..models import Category, Product

class ProductServiceTest(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        self.category = Category.objects.create(
            name = "Electronics",
            description = "Electronic products",
            organisation_id=organisation.organisation_uid
        )

        self.organisation_uid = organisation.organisation_uid
        self.category_service = CategoryService()
        self.product_service = ProductService()

    def test_create_category(self):
        payload = {
            "name": "Electronics",
            "description": "Electronic products"
        }
        new_category = self.category_service.create_category(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_category, Category))
        self.assertEqual(new_category.name, 'Electronics')


    def test_create_product(self):
        str_category = str(self.category.category_uid)
        payload = {
            "name": "Lenovo Thinkpad",
            "description": "Thinkpad mod_001 i3 8GB RAM GRP",
            "category" : str_category
            }

        category = Category.objects.get(
            organisation_id=self.organisation_uid,
            category_uid=str_category,
        )

        self.assertTrue(isinstance(category, Category))
        new_product = self.product_service.create_product(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_product, Product))
        self.assertEqual(new_product.name , "Lenovo Thinkpad")

