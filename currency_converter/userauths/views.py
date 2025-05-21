from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

import random
from django.core.mail import send_mail
from django.conf import settings

from django.http import HttpResponseRedirect

from .forms import UserRegistrationForm, UserLoginForm

User = get_user_model()

'''def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('userauths:register')

        # Create the user
        user = User.objects.create_user(
            username=email,  # Use email as the username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Log the user in and redirect to the dashboard
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('converter:dashboard')
    
    return render(request, 'userauths/register.html')'''
    

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('userauths:register')

        # Create the user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create accounts for the user
        from .utils import generate_account_details
        generate_account_details(user)

        # Log the user in and redirect to the dashboard
        login(request, user)
        messages.success(request, 'Registration successful! Your accounts have been created.')
        return redirect('converter:dashboard')
    
    return render(request, 'userauths/register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #form = UserLoginForm(data=request.POST)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user = request.user
            print("====================")
            print(user.first_name)
            messages.success(request, 'Login successful!')
            return redirect('converter:dashboard') 
    #else: form = UserLoginForm()
    return render(request, 'userauths/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('converter:index')  # Redirect to the login page or any other page


def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP

def send_otp_to_email(user):
    otp = generate_otp()
    user.otp = otp
    user.save()

    # Send OTP via email
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP for password reset is: {otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


#Request OTP for password reset
def request_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_otp_to_email(user)
            messages.success(request, 'OTP sent to your email!')
            return redirect('userauths:verify_otp') 
        except User.DoesNotExist:
            messages.error(request, 'Email not registered.')
    return render(request, 'userauths/request_otp.html')

#Verify OTP and reset password
def validate_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email, otp=otp)
            user.set_password(new_password)
            user.otp = None  # Clear the OTP after successful verification
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('userauths:login') 
        except User.DoesNotExist:
            messages.error(request, 'Invalid OTP or email.')
    return render(request, 'userauths/verify_otp.html')

from django.contrib.auth.hashers import make_password

def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)  # Hash the new password
            user.otp = None  # Erase the OTP
            user.save()
            messages.success(request, 'Password reset successful. You can now log in.')
            return redirect('userauths:login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
    return render(request, 'userauths/reset_password.html')