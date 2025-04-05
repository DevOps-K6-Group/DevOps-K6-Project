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
    account_gbp = models.CharField(max_length=20, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    def generate_account_details(self):
        """
        Generate unique account details for USD and GBP and assign them to the user.
        """
        if not self.account_usd:
            self.account_usd = f"USD-{uuid.uuid4().hex[:12].upper()}"
        if not self.account_gbp:
            self.account_gbp = f"GBP-{uuid.uuid4().hex[:12].upper()}"
        self.save()