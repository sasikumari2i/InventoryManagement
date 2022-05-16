import io
from datetime import date, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from ..payments.models import Invoice
from organisations.models import Organisation
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class CategoryService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data, organisation):
        """Creates new order from the given data"""

        try:
            new_category = Category.objects.create(name=validated_data.data['name'],
                                                   description=validated_data.data['description'],
                                                   organisation_id=organisation)
            return new_category
        except KeyError:
            raise CustomException(400,"Invalid details")


class ProductService:

    @transaction.atomic()
    def create(self, validated_data, organisation):
        """Creates new order from the given data"""
        try:
            category = Category.objects.get(organisation_id=organisation,id=validated_data.data['category'])
            new_product = Product.objects.create(name=validated_data.data['name'],
                                                 description=validated_data.data['description'],
                                                 available_stock=validated_data.data['available_stock'],
                                                 price=validated_data.data['price'],
                                                 category_id=validated_data.data['category'],
                                                 organisation_id=organisation)
            return new_product
        except Category.DoesNotExist:
            raise CustomException(404, "Category not available")

