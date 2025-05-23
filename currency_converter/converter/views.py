import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
import requests
from .models import Transaction

User = get_user_model()


def index(request):
    return render(request, 'converter/index.html')


def dashboard_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:login')
    
    # Get the user object
    user = User.objects.get(id=request.user.id)
    
    # Get recent transactions (limited to 5)
    from django.db.models import Q
    recent_transactions = Transaction.objects.filter(
        Q(user=user) | Q(recipient=user)
    ).select_related('user', 'recipient').order_by('-created_at')[:5]
    
    # Count total transactions
    total_transactions = Transaction.objects.filter(
        Q(user=user) | Q(recipient=user)
    ).count()
    
    # Create context with user data
    context = {
        'user': user,
        'usd_balance': user.balance_usd,
        'gbp_balance': user.balance_gbp,
        # Account details
        'usd_account': user.account_usd,
        'usd_routing': user.routing_usd,
        'gbp_account': user.account_gbp,
        'gbp_sort_code': user.sort_code_gbp,
        
        'total_transactions': total_transactions,  
        'recent_transactions': recent_transactions  
    }
    
    return render(request, 'converter/dashboard.html', context)


@login_required
def transaction_history(request):
    """View function to fetch and display transaction history for the current user"""
    # Get transactions where the user is either the sender or recipient
    user_transactions = Transaction.objects.filter(
        models.Q(user=request.user) | models.Q(recipient=request.user)
    ).select_related('user', 'recipient').order_by('-created_at')
    
    # Create context with user data and transactions
    context = {
        'transactions': user_transactions,
        'user': request.user,
        'usd_balance': request.user.balance_usd,
        'gbp_balance': request.user.balance_gbp,
    }
    
    return render(request, 'converter/transaction_history.html', context)


def convert(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        amount = float(data.get('amount'))
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')

        # API details
        api_key = settings.API_KEY
        api_url = settings.API_URL

        try:
            # Fetch exchange rates with USD as base
            usd_url = f"{api_url}{api_key}/latest/{from_currency}"
            usd_response = requests.get(usd_url)
            usd_response.raise_for_status()
            usd_data = usd_response.json()

            if usd_data and usd_data.get('result') == 'success':
                exchange_rate = usd_data['conversion_rates'][to_currency]
                converted_amount = amount * exchange_rate

                return JsonResponse({'success': True, 'converted_amount': converted_amount})
            else:
                error_message = usd_data.get('error-type', 'An error occurred.')
                return JsonResponse({'success': False, 'error': error_message})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def convert_view(request, from_currency=None, to_currency=None):
    if request.method == 'POST':
        # Parse body if present
        data = json.loads(request.body)
        amount = float(data.get('amount'))
        
        # URL parameters override any provided in the body
        from_currency = data.get('from_currency', from_currency)
        to_currency = data.get('to_currency', to_currency)
        
        # Get user object
        user = request.user
        
        # Check for sufficient balance
        if from_currency == 'USD':
            if amount > float(user.balance_usd):
                return JsonResponse({'success': False, 'error': 'Insufficient USD balance'})
        elif from_currency == 'GBP':
            if amount > float(user.balance_gbp):
                return JsonResponse({'success': False, 'error': 'Insufficient GBP balance'})
        
        # API details
        api_key = settings.API_KEY
        api_url = settings.API_URL

        try:
            # Fetch exchange rates with from_currency as base
            url = f"{api_url}{api_key}/latest/{from_currency}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data and data.get('result') == 'success':
                exchange_rate = data['conversion_rates'][to_currency]
                converted_amount = amount * exchange_rate
                
                # Update user balances
                if from_currency == 'USD' and to_currency == 'GBP':
                    user.balance_usd = float(user.balance_usd) - amount
                    user.balance_gbp = float(user.balance_gbp) + converted_amount
                elif from_currency == 'GBP' and to_currency == 'USD':
                    user.balance_gbp = float(user.balance_gbp) - amount
                    user.balance_usd = float(user.balance_usd) + converted_amount
                
                # Save the updated user object
                user.save()

                transaction = Transaction.objects.create(
                    user=user,
                    transaction_type='CONVERSION',
                    amount=amount,
                    currency=from_currency,
                    converted_amount=converted_amount,
                    converted_currency=to_currency,
                    description=f"Converted {from_currency} to {to_currency}",
                    status='COMPLETED'
                )
                
                return JsonResponse({
                    'success': True, 
                    'converted_amount': converted_amount,
                    'exchange_rate': exchange_rate,
                    'new_balance_from': float(user.balance_usd if from_currency == 'USD' else user.balance_gbp),
                    'new_balance_to': float(user.balance_gbp if to_currency == 'GBP' else user.balance_usd)
                })
            else:
                error_message = data.get('error-type', 'An error occurred.')
                return JsonResponse({'success': False, 'error': error_message})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Handle GET requests
    elif request.method == 'GET':
        # Return current exchange rate info without performing transaction
        api_key = settings.API_KEY
        api_url = settings.API_URL
        
        try:
            url = f"{api_url}{api_key}/latest/{from_currency}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and data.get('result') == 'success':
                exchange_rate = data['conversion_rates'][to_currency]
                return JsonResponse({
                    'success': True,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'exchange_rate': exchange_rate
                })
            else:
                return JsonResponse({'success': False, 'error': 'Failed to fetch exchange rate'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def transfer_money(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body)
            amount = float(data.get('amount', 0))
            recipient_email = data.get('recipient_email')
            currency = data.get('currency')  # 'USD' or 'GBP'
            
            # Validate the data
            if amount <= 0:
                return JsonResponse({'success': False, 'error': 'Amount must be greater than zero'})
            
            if not recipient_email:
                return JsonResponse({'success': False, 'error': 'Recipient email is required'})
                
            if currency not in ['USD', 'GBP']:
                return JsonResponse({'success': False, 'error': 'Invalid currency'})
            
            # Get the sender (current user) and recipient
            sender = request.user
            
            try:
                recipient = User.objects.get(email=recipient_email)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Recipient not found'})
                
            # Check if sender is trying to send money to themselves
            if sender.id == recipient.id:
                return JsonResponse({'success': False, 'error': 'Cannot transfer money to yourself'})
            
            # Check if sender has sufficient balance
            if currency == 'USD':
                if amount > float(sender.balance_usd):
                    return JsonResponse({'success': False, 'error': 'Insufficient USD balance'})
                
                # Perform the transfer
                sender.balance_usd = float(sender.balance_usd) - amount
                recipient.balance_usd = float(recipient.balance_usd) + amount
            else:  # GBP
                if amount > float(sender.balance_gbp):
                    return JsonResponse({'success': False, 'error': 'Insufficient GBP balance'})
                
                # Perform the transfer
                sender.balance_gbp = float(sender.balance_gbp) - amount
                recipient.balance_gbp = float(recipient.balance_gbp) + amount
            
            # Save the changes
            sender.save()
            recipient.save()


            transaction = Transaction.objects.create(
                user=sender,
                recipient=recipient,
                transaction_type='TRANSFER',
                amount=amount,
                currency=currency,
                description=f"Transfer to {recipient.email}",
                status='COMPLETED'
            )
            
            # Return success response
            return JsonResponse({
                'success': True,
                'message': f'Successfully transferred {currency} {amount} to {recipient.email}',
                'new_balance': float(sender.balance_usd if currency == 'USD' else sender.balance_gbp)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # If not POST request
    return JsonResponse({'success': False, 'error': 'Invalid request method'})