import random
import string
import uuid

def generate_account_details(user):
    """
    Generate unique account details for USD and GBP accounts for a user
    using purely numeric account numbers
    """
    # Generate USD account ID if not already set
    if not user.account_usd:
        user.account_usd = ''.join(random.choice(string.digits) for _ in range(10))
        user.routing_usd = ''.join(random.choice(string.digits) for _ in range(9))
        user.balance_usd = 1000.00
    
    # Generate GBP account ID if not already set
    if not user.account_gbp:
        user.account_gbp = ''.join(random.choice(string.digits) for _ in range(8))
        user.sort_code_gbp = f"{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        user.balance_gbp = 800.00
    
    user.save()
    
    return user