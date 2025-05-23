from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('convert/', views.convert, name='convert'),
    
    # Make sure this URL pattern accepts parameters:
    path('convert_view/<str:from_currency>/<str:to_currency>/', views.convert_view, name='convert_view'),
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('transactions/', views.transaction_history, name='transaction_history'),
]