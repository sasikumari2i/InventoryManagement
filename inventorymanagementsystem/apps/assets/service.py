import io
from datetime import date, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from .serializers import AssetSerializer, RepairingStockSerializer
from .models import Asset, RepairingStock
from ..products.models import Product,Category
from ..payments.models import Invoice
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class AssetService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data):
        """Creates new order from the given data"""

        try:
            products = Product.objects.filter(organisation=validated_data.data['organisation'])
            customer = Customer.objects.get(organisation=validated_data.data['organisation'],
                                            id=validated_data.data['customer'])
            return customer
            # new_order = Order.objects.create(is_sales_order=validated_data.data['is_sales_order'],
            #                                  delivery_date=validated_data.data['delivery_date'],
            #                                  vendors_id=validated_data.data['vendors'],
            #                                  customers_id=validated_data.data['customers'])
            #
            # for product in order_products:
            #     product_details = products.get(id=product['product'])
            #     if validated_data.data['is_sales_order'] and product_details.available_stock >= product['quantity']:
            #         product_details.available_stock = product_details.available_stock - product['quantity']
            #     elif not validated_data.data['is_sales_order']:
            #         product_details.available_stock = product_details.available_stock + product['quantity']
            #     else:
            #         raise CustomException(400,"Enter only available stock")
            #     product_details.save()
            #     order_product_data = OrderProduct.objects.create(order=new_order, product=product_details,
            #                                                      quantity=product['quantity'])
            #
            # invoice = self.create_invoice(new_order)
            # invoice.save()
            # order_product_data.save()
            # new_order.save()
            # return new_order
        except KeyError as exc:
            raise CustomException(400, "Exception in Order Creation")
        except Product.DoesNotExist:
            raise CustomException(400, "Please enter available products only")
