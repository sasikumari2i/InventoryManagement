from django.test import TestCase

from ..service import CategoryService
from ..serializers import CategorySerializer
from organisations.models import Organisation
from ..models import Category

class ProductServiceTest(TestCase):

    # def test_create_category(self):
    #     result = self.client.post(self.categories_url)
    #     self.assertEqual(result.status_code, 400)


    def setUp(self):
        self.organisation = Organisation.objects.create(
            name='Ideas2it',
            description='Ideas2it Organisation'
        )

        self.organisation_uid = self.organisation.organisation_uid

    # def mocked_create(self):
    #     return self.category

    # @mock.patch('apps.products.models.Category.objects.create',
    #             side_effect=mocked_create)
    # @mock.patch('apps.products.models.Category.objects.create',
    #             return_value=Category.objects.filter(id=1))
    def test_create_category(self):
        category_service = CategoryService()
        category_dict = {
            "name" : "Electronics",
            "description" : "Electronic products"
        }
        serialized_data = CategorySerializer(category_dict)
        # self.organisation_uid = self.organisation.organisation_uid
        result = category_service.create_category(serialized_data, self.organisation_uid)
        # print(result.id)
        self.assertTrue(isinstance(result, Category))
        self.assertEqual(result.name, 'Electronics')
        # self.assertEqual(category.name,'Electronics')
        # self.assertEqual(category.description, 'Electronic products')
        # self.assertEqual(category.organisation_id, organisation_uid)

    # def test_create_category(self):
    #
    #     organisation_uid = self.organisation.organisation_uid
    #     category = Category.objects.create(
    #         id=1, name='Lenovo Thinkpad',
    #         description='Lenovo Thinkpad i7 8GB RAM',
    #         category_id=,
    #         organisation_id=organisation_uid
    #     )
    #     name = validated_data.data["name"],
    #     description = validated_data.data["description"],
    #     category_id = validated_data.data["category"],
    #     organisation_id = organisation,
    #     self.assertTrue(isinstance(category, Category))
    #     self.assertEqual(category.id, 1)
    #     self.assertEqual(category.name,'Electronics')
    #     self.assertEqual(category.description, 'Electronic products')
    #     self.assertEqual(category.organisation_id, organisation_uid)

