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

User = get_user_model()


def index(request):
    return render(request, 'converter/index.html')


def dashboard_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('userauths:login')
    
    # Get the user object
    user = User.objects.get(id=request.user.id)
    
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

        'total_transactions': 0,  
        'recent_transactions': []  
    }
    
    return render(request, 'converter/dashboard.html', context)

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