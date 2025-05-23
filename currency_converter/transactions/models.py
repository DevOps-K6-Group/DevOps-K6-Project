from django.db import models
from userauths.models import User

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='transactions_received_transactions'  # Changed this
    )
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    amount_gbp = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver} on {self.timestamp}"