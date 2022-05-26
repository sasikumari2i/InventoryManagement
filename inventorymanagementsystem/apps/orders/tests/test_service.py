from django.test import TestCase
from unittest import mock
from ..service import CustomerService, VendorService
from ..serializers import CustomerSerializer, VendorSerializer
from organisations.models import Organisation
from ..models import Customer, Vendor

class OrderServiceTest(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        # self.category = Category.objects.create(
        #     name = "Electronics",
        #     description = "Electronic products",
        #     organisation_id=organisation.organisation_uid
        # )

        self.organisation_uid = organisation.organisation_uid
        self.customer_service = CustomerService()

    def test_create_customer(self):
        payload = {
            "name": "Sasi",
            "address": "Chennai",
            "email": "sasi@gmail.com",
            "phone_number": "8789878916"
        }c
        new_customer = self.customer_service.create(payload, self.organisation_uid)
        self.assertTrue(isinstance(new_customer, Customer))
        self.assertEqual(new_customer.name, 'Sasi')


    # def test_create_product(self):
    #     str_category = str(self.category.category_uid)
    #     payload = {
    #         "name": "Lenovo Thinkpad",
    #         "description": "Thinkpad mod_001 i3 8GB RAM GRP",
    #         "category" : str_category
    #         }
    #
    #     category = Category.objects.get(
    #         organisation_id=self.organisation_uid,
    #         category_uid=str_category,
    #     )
    #
    #     self.assertTrue(isinstance(category, Category))
    #     new_product = self.product_service.create_product(payload, self.organisation_uid)
    #     self.assertTrue(isinstance(new_product, Product))
    #     self.assertEqual(new_product.name , "Lenovo Thinkpad")
