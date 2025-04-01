from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert, name='convert'),  # Add this line
    #path('convert/<str:from_currency>/<str:to_currency>/<float:amount>/', views.convert, name='convert'),  # Add this line
    #path('convert/<str:from_currency>/<str:to_currency>/', views.convert, name='convert'),  # Add this line
    #path('convert/<str:from_currency>/', views.convert, name='convert'),  # Add this line
]