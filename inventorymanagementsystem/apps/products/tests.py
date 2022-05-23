from django.test import TestCase
from unittest import mock

from .service import CategoryService
from organisations.models import Organisation
from .models import Category

class CategoryServiceTest(TestCase):

    def setUp(self):
        self.organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        organisation_uid = self.organisation.organisation_uid
        self.category = Category.objects.create(
            id=1, name='Electronics',
            description='Electronic products',
            organisation_id=organisation_uid
        )

    @mock.patch('apps.products.models.Category.objects.create',
                return_value=Category.objects.filter(id=1))
    def test_create(self, mock_create):
        self.assertEqual(self.category, mock_create.return_value[0])