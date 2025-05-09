from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
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