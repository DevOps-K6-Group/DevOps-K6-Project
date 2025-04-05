from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout

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
        amount = request.POST.get('amount')
        from_currency = request.POST.get('from_currency')
        # Add logic for currency conversion here
        return JsonResponse({'success': True, 'converted_amount': 100})  # Example response
    return JsonResponse({'success': False, 'error': 'Invalid request method'})