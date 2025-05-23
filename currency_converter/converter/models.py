from django.db import models
from userauths.models import User

#User = get_user_model()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('TRANSFER', 'Transfer'),
        ('CONVERSION', 'Currency Conversion'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]
    
    STATUS_CHOICES = [
        ('COMPLETED', 'Completed'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='converter_transactions')
    recipient = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='converter_received_transactions'  # Changed this
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # USD, GBP, etc.
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    converted_currency = models.CharField(max_length=3, null=True, blank=True)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.currency} {self.amount} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
