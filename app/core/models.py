from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    # The "**" lets you collect any additional fields into this function
    # without having to change it each time you need a new field
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        # Create a new user model and assign it to the user variable
        # the "normalize_email" helper function that comes with the
        # BaseUserManager
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # the "using=self._db" is good practice because it allows you to use
        # multiple db's
        user.save(using=self._db)
        return user

    # don't have to worry about the extra fields here because we will only
    # create superusers with the command line
    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using an email instead of a username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # this is 'username' by default, and so we want to change it to email
    USERNAME_FIELD = 'email'
