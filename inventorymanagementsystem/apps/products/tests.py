from django.test import TestCase
from unittest import mock

from .service import CategoryService
from organisations.models import Organisation
from .models import Category

class CategoryServiceTest(TestCase):

    # def setUp(self):
    #     self.organisation = Organisation.objects.create(
    #         name='Ideas2it',
    #         description='Ideas2it Organisation'
    #     )
    #
    #     organisation_uid = self.organisation.organisation_uid
    #     self.category = Category.objects.create(
    #         id=1, name='Electronics',
    #         description='Electronic products',
    #         organisation_id=organisation_uid
    #     )

    # @mock.patch('apps.products.models.Category.objects.create',
    #             return_value=Category.objects.filter(id=1))
    def test_create(self):

        organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        organisation_uid = organisation.organisation_uid
        category = Category.objects.create(
            id=1, name='Electronics',
            description='Electronic products',
            organisation_id=organisation_uid
        )
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name,'Electronics')
        self.assertEqual(category.description, 'Electronic products')
        self.assertEqual(category.organisation_id, organisation_uid)

