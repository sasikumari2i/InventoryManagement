import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import Application, AbstractApplication
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from oauth2_provider.models import AbstractApplication, Application

# Create your models here.
from organisations.models import Organisation


class MyUserManager(BaseUserManager):

    def create_user(self, name, phone_no, email, password=None):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            phone_no=phone_no,
            is_superuser=True)
        user.set_password(password)
        user.save(using=self._db)
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name
        )
        application.save()
        return user

    def create_superuser(self, name, phone_no, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name=name, phone_no=phone_no,
                                email=email, password=password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # ROLE_CHOICES = [
    #     ("super_user", "super_user"),
    #     ("staff", "staff"),
    # ]

    user_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10)
    # is_super_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.UUIDField(default=None, null=True)
    # user_role = models.CharField(choices=ROLE_CHOICES,
    #                              default="staff",
    #                              max_length=15)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
        null=True
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_no']

    def __str__(self):
        return "{}".format(self.email)

