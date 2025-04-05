from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ExchangeCurrencyForm, TransferMoneyForm
from .models import Transaction
from userauths.models import User

@login_required
def exchange_currency_view(request):
    if request.method == 'POST':
        form = ExchangeCurrencyForm(request.POST)
        if form.is_valid():
            amount_usd = form.cleaned_data['amount_usd']
            if request.user.balance_usd >= amount_usd:
                amount_gbp = amount_usd * settings.EXCHANGE_RATES['USD_TO_GBP']
                request.user.balance_usd -= amount_usd
                request.user.balance_gbp += amount_gbp
                request.user.save()
                Transaction.objects.create(sender=request.user, amount_usd=amount_usd, amount_gbp=amount_gbp)
                return redirect('dashboard')
    else:
        form = ExchangeCurrencyForm()
    return render(request, 'transactions/exchange.html', {'form': form})

@login_required
def transfer_money_view(request):
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver_username']
            amount_usd = form.cleaned_data['amount_usd']
            try:
                receiver = User.objects.get(username=receiver_username)
                if request.user.balance_usd >= amount_usd:
                    request.user.balance_usd -= amount_usd
                    receiver.balance_usd += amount_usd
                    request.user.save()
                    receiver.save()
                    Transaction.objects.create(sender=request.user, receiver=receiver, amount_usd=amount_usd, amount_gbp=0)
                    return redirect('dashboard')
            except User.DoesNotExist:
                form.add_error('receiver_username', 'User does not exist')
    else:
        form = TransferMoneyForm()
    return render(request, 'transactions/transfer.html', {'form': form})