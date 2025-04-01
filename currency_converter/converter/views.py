from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'converter/index.html')


def convert(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        from_currency = request.POST.get('from_currency')
        # Add logic for currency conversion here
        return JsonResponse({'success': True, 'converted_amount': 100})  # Example response
    return JsonResponse({'success': False, 'error': 'Invalid request method'})