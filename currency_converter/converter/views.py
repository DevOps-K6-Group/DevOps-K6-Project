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


@login_required
def dashboard_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    return render(request, 'converter/dashboard.html', {'user': user})



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