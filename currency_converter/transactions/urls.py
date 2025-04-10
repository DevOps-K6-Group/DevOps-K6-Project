from django.urls import path
from .views import exchange_currency_view, transfer_money_view

app_name = 'transactions'

urlpatterns = [
    path('exchange/', exchange_currency_view, name='exchange_currency'),
    path('transfer/', transfer_money_view, name='transfer_money'),
]