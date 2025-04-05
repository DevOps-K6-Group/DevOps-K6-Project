from django.urls import path
from .views import logout_view, register_view, login_view
from .views import request_otp_view, validate_otp_view, reset_password_view

app_name = 'userauths'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('request-otp/', request_otp_view, name='request_otp'),
    path('validate-otp/', validate_otp_view, name='validate_otp'),
    path('reset-password/', reset_password_view, name='reset_password'),
    #path('dashboard/', dashboard_view, name='dashboard'),
]