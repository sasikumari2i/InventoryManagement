import sys
from rest_framework import serializers
import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Vendor, Order, OrderProduct, Customer
from ..products.models import Product
import utils.exceptionhandler as exceptionhandler
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "customer_uid",
            "name",
            "address",
            "email",
            "phone_number",
            "created_date",
            "updated_date",
        )


class OrderProductSerializer(serializers.ModelSerializer):

    price = serializers.FloatField(source="product.price")

    class Meta:
        model = OrderProduct
        fields = ("product", "quantity", "price")


class OrderInvoiceSerializer(serializers.ModelSerializer):

    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "order_uid",
            "order_products",
        )


class OrderSerializer(serializers.ModelSerializer):

    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "order_uid",
            "order_date",
            "delivery_status",
            "delivery_date",
            "vendors",
            "order_products",
            "invoice",
        )

    def validate(self, data):
        """Validations for the Order model"""

        try:
            if self.initial_data["vendors"] is None:
                raise CustomException(400, "Please give vendor details for the order")

            try:
                delivery_date = datetime.datetime.strptime(
                    self.initial_data["delivery_date"], "%Y-%m-%d"
                )
                if delivery_date < datetime.datetime.today():
                    raise CustomException(
                        400, "Order date cannot be greater than Delivery date"
                    )
            except KeyError:
                data["delivery_date"] = date.today() + timedelta(days=15)

            return data
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)


class VendorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Vendor
        fields = (
            "vendor_uid",
            "name",
            "address",
            "email",
            "phone_number",
            "created_date",
            "updated_date",
        )


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("order_uid",)
