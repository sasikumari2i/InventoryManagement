from datetime import date, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
import base64

from .serializers import OrderSerializer
from .models import Order, OrderProduct, Vendor, Customer
from ..products.models import Product, Inventory
from ..payments.models import Invoice
from utils.exceptionhandler import CustomException


class OrderService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data, order_products, organisation_uid):
        """Creates new order from the given data"""

        try:
            products = Product.objects.filter(organisation_id=organisation_uid)
            vendor = Vendor.objects.get(vendor_uid=validated_data["vendors"],
                                        organisation_id=organisation_uid)
            new_order = Order.objects.create(
                delivery_date=validated_data["delivery_date"],
                vendors_id=validated_data["vendors"],
                organisation_id=organisation_uid,
            )

            for product in order_products:
                product_details = products.get(product_uid=product["product"])
                product_details.price = product["price"]
                product_details.available_stock = (
                    product_details.available_stock + product["quantity"]
                )
                product_details.save()
                order_product_data = OrderProduct.objects.create(
                    order=new_order,
                    product=product_details,
                    quantity=product["quantity"],
                )
                inventories = self.create_inventory(product['inventory'],
                                                    product_details.product_uid,
                                                    product["quantity"])
            invoice = self.create_invoice(new_order, organisation_uid)
            invoice.save()
            order_product_data.save()
            new_order.save()
            return new_order
        except KeyError:
            raise CustomException(400, "Exception in Order Creation")
        except Product.DoesNotExist:
            raise CustomException(400, "Please enter available products only")
        except Vendor.DoesNotExist:
            raise CustomException(400, "Invalid Vendor")

    def create_inventory(self, inventories,product_uid, quantity):
        """Read employees.txt file as csv and convert
        into the list of employee dictionary
        """
        csv_file = base64.b64decode(inventories).decode()
        csv_list = [word.split(',') for word in csv_file.split('\n')]
        products = list()
        # heading = list()
        line_count = 0
        if not len(csv_list) == quantity:
            raise CustomException(400, "Please serial numbers not matching count of product")
        for row in csv_list:
            if line_count == 0:
                # heading = row
                line_count = 1
            else:
                inventory = Inventory(serial_no=row[0],product_id=product_uid)
                products.append(inventory)

        inventories = Inventory.objects.bulk_create(products)
        return inventories

    # @transaction.atomic
    # def update(self, order_details, validated_data, order_products, organisation_uid):
    #     """Updates details of the given order"""
    #
    #     try:
    #         products = Product.objects.filter(organisation_id=organisation_uid)
    #         vendor = Vendor.objects.get(vendor_uid=validated_data["vendors"],
    #                                     organisation_id=organisation_uid)
    #         product_orders = OrderProduct.objects.all()
    #         order_details.delivery_date = validated_data["delivery_date"]
    #         order_details.vendors_uid = validated_data["vendors"]
    #         order_details.save()
    #
    #         for product in order_products:
    #             product_details = products.get(product_uid=product["product"])
    #             old_order_product = product_orders.get(
    #                 product=product_details.product_uid, order=order_details.order_uid
    #             )
    #             old_quantity = old_order_product.quantity
    #             product_details.available_stock = (
    #                 product_details.available_stock - old_quantity
    #             )
    #             product_details.available_stock = (
    #                 product_details.available_stock + product["quantity"]
    #             )
    #             product_details.price = product["price"]
    #             product_details.save()
    #             order_product_details = product_orders.get(
    #                 product=product_details.product_uid, order=order_details.order_uid
    #             )
    #             order_product_details.product = product_details
    #             order_product_details.order = order_details
    #             order_product_details.quantity = product["quantity"]
    #             order_product_details.save()
    #
    #         return order_details
    #     except KeyError as exc:
    #         raise CustomException(400, "Exception in Order Update")
    #     except CustomException as exc:
    #         raise CustomException(exc.status_code, exc.detail)
    #     except Vendor.DoesNotExist:
    #         raise CustomException(404, "Vendor does not exist")
    #     except Product.DoesNotExist:
    #         raise CustomException(404, "Product does not exist")

    def create_invoice(self, new_order, organisation_uid):
        """Creates invoice for the created order"""

        try:
            amount = 0
            products = Product.objects.filter(organisation_id=organisation_uid)
            order_serializer = OrderSerializer(new_order)
            for orders in order_serializer.data["order_products"]:
                product = products.get(product_uid=orders["product"])
                product_price = orders["price"]
                product_quantity = orders["quantity"]
                amount = amount + (product_price * product_quantity)

            created_date = date.today()
            payment_deadline = created_date + timedelta(days=15)
            invoice = Invoice.objects.create(
                amount=amount,
                created_date=created_date,
                payment_deadline=payment_deadline,
                order=new_order,
                organisation_id=new_order.organisation_id,
            )
            return invoice
        except ValidationError as exc:
            raise CustomException(400, "Exception in PO Invoice Creation")

    def update_delivery(self, order_details):
        """Updates the delivery status of the given order"""

        try:
            delivery_status = order_details.delivery_status
            response = {}
            if delivery_status:
                response = {"message": "It is already delivered"}
            elif not delivery_status:
                order_details.delivery_status = True
                order_details.save()
                response = {"message": "Delivery Status Updated"}
            return response
        except NotFound:
            raise CustomException(400, "Internal error in updating delivery status")


class VendorService:
    """Performs vendor related operations like add new vendor, get single vendor,
        get all vendors, update a vendor and delete vendor"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new vendor from the given data"""

        try:
            new_vendor = Vendor.objects.create(
                name=validated_data["name"],
                address=validated_data["address"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                organisation_id=organisation_uid,
            )
            return new_vendor
        except KeyError:
            raise CustomException(400, "Invalid details")


class CustomerService:
    """Performs customer related operations like add new customer, get single customer,
            get all customers, update a customer and delete customer"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new customer from the given data"""

        try:
            new_customer = Customer.objects.create(
                name=validated_data["name"],
                address=validated_data["address"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                organisation_id=organisation_uid,
            )
            return new_customer
        except KeyError:
            raise CustomException(400, "Invalid details")
