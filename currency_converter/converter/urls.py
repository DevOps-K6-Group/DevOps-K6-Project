from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    #path('login', views.login, name='login'),
    #path('register', views.register, name='register'),
    path('convert/', views.convert, name='convert'), 
    path('convert_view/', views.convert_view, name='convert_view'), 
    #path('convert/<str:from_currency>/<str:to_currency>/<float:amount>/', views.convert, name='convert'),  # Add this line
    #path('convert/<str:from_currency>/<str:to_currency>/', views.convert, name='convert'),  # Add this line
    #path('convert/<str:from_currency>/', views.convert, name='convert'),  # Add this line
]