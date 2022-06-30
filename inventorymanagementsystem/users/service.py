from django.db import transaction
from django.core.exceptions import ValidationError
from oauth2_provider.models import Application

from .models import User
from organisations.models import Organisation
from utils.exceptionhandler import CustomException


class UserService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, user, created_by, password):
        """Creates new order from the given data"""

        try:
            new_user = User.objects.create(
                name=user.data['name'],
                email=user.data['email'],
                phone_no=user.data['phone_no'],
                created_by=created_by,
                organisation_id=user.data['organisation']
            )
            new_user.set_password(password)
            new_user.save()
            application = Application.objects.create(
                user=new_user,
                authorization_grant_type='password',
                client_type="public",
                name=new_user.name
            )
            application.save()
            return new_user
        except KeyError:
            raise CustomException(400, "Invalid details")
        except Organisation.DoesNotExist:
            raise CustomException(400, "Organisation does not exist")
        except ValidationError:
            raise CustomException(400, "Organisation does not exist")