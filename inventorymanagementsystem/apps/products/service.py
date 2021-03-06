from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Product, Category
from organisations.models import Organisation
from utils.exceptionhandler import CustomException


class CategoryService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create_category(self, validated_data, organisation_uid):
        """Creates new order from the given data"""

        try:
            new_category = Category.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                organisation_id=organisation_uid,
            )
            return new_category
        except KeyError:
            raise CustomException(400, "Invalid details")
        except Organisation.DoesNotExist:
            raise CustomException(400, "Organisation does not exist")
        except ValidationError:
            raise CustomException(400, "Organisation does not exist")


class ProductService:
    @transaction.atomic()
    def create_product(self, validated_data, organisation):
        """Creates new order from the given data"""
        try:
            category = Category.objects.get(
                organisation_id=organisation, category_uid=validated_data["category"],
            )
            new_product = Product.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                category_id=validated_data["category"],
                organisation_id=organisation,
            )
            return new_product
        except KeyError:
            raise CustomException(400, "Invalid details")
        except ValidationError:
            raise CustomException(400, "Invalid details")
