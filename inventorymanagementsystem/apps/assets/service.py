from datetime import date
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError
import datetime
from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError

from .models import Asset, RepairingStock
from ..orders.models import Customer
from .serializers import AssetSerializer
from ..products.models import Product, Category, Inventory
from utils.exceptionhandler import CustomException


class AssetService:
    """Performs asset related operations like add new asset for a customer,
    update asset details"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new Asset from the given data"""

        try:
            inventory = Inventory.objects.get(
                organisation_id=organisation_uid, product_id=validated_data["product"],
                serial_no=validated_data["serial_no"],
                is_available=True
            )
            customer = Customer.objects.get(
                organisation_id=organisation_uid,
                customer_uid=validated_data["customer"],
            )

            try:
                asset = Asset.objects.get(
                    inventory_id=inventory.inventory_uid,
                    is_active=True,
                    organisation_id=organisation_uid
                )
                raise CustomException(400, "This product is already assigned")
            except Asset.DoesNotExist:
                pass

            # if product.available_stock <= 0:
            #     raise CustomException(400, "Product is out of Stock")
            new_asset = Asset.objects.create(
                inventory_id=inventory.inventory_uid,
                customer_id=validated_data["customer"],
                organisation_id=organisation_uid,
            )
            product = Product.objects.get(product_uid=validated_data["product"],
                                          organisation_id=organisation_uid)
            product.available_stock -= 1
            inventory.is_available = False
            inventory.updated_date = date.today()
            product.save()
            inventory.save()
            return new_asset
        except KeyError as exc:
            raise CustomException(400, "Exception in Asset Service")
        except Inventory.DoesNotExist:
            raise CustomException(400, "Invalid Product")
        except Customer.DoesNotExist:
            raise CustomException(400, "Invalid Customer")
        except Product.DoesNotExist:
            raise CustomException(400, "Invalid Product")

    @transaction.atomic()
    def update(self, instance, request):
        """Updates the Asset from the given data"""

        try:
            if not instance.is_active:
                raise CustomException(400, "Only active assets can be updated")
            customer = Customer.objects.get(
                customer_uid=request["customer"], organisation_id=instance.organisation
            )
            product = Product.objects.get(product_uid=request["product"],
                                         organisation_id=instance.organisation)
            inventory = Inventory.objects.get(
                product_id=request["product"],
                serial_no=request["serial_no"],
                is_available=True,
                organisation_id=instance.organisation
            )
            instance.updated_date = date.today()
            if inventory.inventory_uid != instance.inventory_id:
                old_inventory = Inventory.objects.get(inventory_uid=instance.inventory_id)
                old_inventory.is_available= True
                old_inventory.updated_date = date.today()
                old_inventory.save()
                inventory.is_available = False
                instance.inventory_id=inventory.inventory_uid
            inventory.updated_date = date.today()
            inventory.save()
            instance.save()
            return instance
        except Customer.DoesNotExist:
            raise CustomException(404, "Invalid Customer")
        except Product.DoesNotExist:
            raise CustomException(404, "Invalid Product")
        except Inventory.DoesNotExist:
            raise CustomException(404, "Invalid Product")
        except KeyError:
            raise CustomException(400, "Product and Customer is mandatory for updating")

    @transaction.atomic()
    def close_asset(self, asset_details, data):
        """Update Asset status to False"""

        try:
            is_active = asset_details.is_active
            response = {}
            if not is_active:
                response = {"message": "It is already not active"}
            elif is_active:
                asset_details.is_active = False
                asset_details.updated_date = date.today()

                try:
                    returned_date = datetime.datetime.strptime(
                        data["return_date"], "%Y-%m-%d"
                    )
                    if returned_date > datetime.datetime.today():
                        raise CustomException(
                            400, "Returned Date cannot be after today"
                        )
                except KeyError:
                    data["return_date"] = datetime.datetime.today()

                asset_details.return_date = data["return_date"]
                asset_details.save()
                response = {"message": "Assigned asset is closed"}
            return response
        except NotFound:
            raise CustomException(
                400, "Internal error in updating active status in asset"
            )


class RepairingStockService:
    """Performs Repairing Stock related operations like add new repairing stock for an asset,
        update repairing stock details"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new Repairing Stock for the given Asset"""

        try:
            asset = Asset.objects.get(
                organisation_id=organisation_uid, asset_uid=validated_data["asset"]
            )

            try:
                repairing_stock = RepairingStock.objects.get(
                    asset_id=validated_data["asset"]
                )
                raise CustomException(400, "Duplicate Asset")
            except RepairingStock.DoesNotExist:
                pass

            if asset.is_active:
                raise CustomException(
                    400, "Cannot be created, Assigned is still active"
                )
            new_repairing_stock = RepairingStock.objects.create(
                asset_id=validated_data["asset"],
                organisation_id=organisation_uid,
            )
            return new_repairing_stock
        except KeyError as exc:
            raise CustomException(400, "Exception in Repairing Stock Service")
        except Asset.DoesNotExist:
            raise CustomException(400, "Invalid Asset")


    # def update(self, instance, request):
    #     """Updates Repairing Asset for the given data"""
    #
    #     try:
    #         if not instance.is_active:
    #             raise CustomException(
    #                 400, "Only active repairing stocks can be updated"
    #             )
    #         asset = Asset.objects.get(
    #             asset_uid=request["asset"],
    #             product_id=request["product"],
    #             organisation_id=instance.organisation,
    #         )
    #         instance.updated_date = date.today()
    #         return instance
    #     except Asset.DoesNotExist:
    #         raise CustomException(404, "Invalid Asset")

    @transaction.atomic()
    def close_repairing_stock(self, repairing_stock_details, data):
        """Update Reparing status to False and reflects to the product accordingly"""

        try:
            is_active = repairing_stock_details.is_active
            response = {}
            if not is_active:
                response = {"message": "It is already not active"}
            elif is_active:
                repairing_stock_details.is_active = False
                repairing_stock_details.updated_date = date.today()

                try:
                    closed_date = datetime.datetime.strptime(
                        data["closed_date"], "%Y-%m-%d"
                    )
                    if closed_date > datetime.datetime.today():
                        raise CustomException(400, "Closed Date cannot be after today")
                except KeyError:
                    data["closed_date"] = datetime.datetime.today()

                repairing_stock_details.closed_date = data["closed_date"]
                repairing_stock_details.save()
                asset = Asset.objects.get(asset_uid=repairing_stock_details.asset_id)
                inventory = Inventory.objects.get(inventory_uid=asset.inventory_id)
                inventory.is_available = True
                inventory.updated_date = date.today()
                inventory.save()
                product = Product.objects.get(
                    product_uid=inventory.product_id
                )
                product.available_stock = product.available_stock + 1
                product.updated_date = date.today()
                product.save()
                response = {"message": "Repairing Stock asset is closed"}
            return response
        except NotFound:
            raise CustomException(
                400, "Internal error in updating active status in repairing stock"
            )
