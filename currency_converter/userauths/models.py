from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()
    username = None  
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=False) 
    last_name = models.CharField(max_length=30, blank=False) 
    balance_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_gbp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    otp = models.CharField(max_length=6, blank=True, null=True)
    
    account_usd = models.CharField(max_length=20, unique=True, blank=True, null=True)
    routing_usd = models.CharField(max_length=9, blank=True, null=True)  # For US accounts
    
    account_gbp = models.CharField(max_length=20, unique=True, blank=True, null=True)
    sort_code_gbp = models.CharField(max_length=8, blank=True, null=True)  # For UK accounts
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email  