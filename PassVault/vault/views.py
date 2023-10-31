from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
import string

def display_error_message(request, errors):
    error_messages = [error for field, error in errors.items()]
    for error in error_messages:
        messages.error(request, error)

def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully registered.')
            return redirect('login')
        else:
            display_error_message(request, form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'You are logged in.')
                return redirect('index')
        messages.error(request, 'Wrong credentials!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('index')
        else:
            display_error_message(request, form.errors) 
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form':form})

@login_required(login_url='login')
def init_email_change(request):
    if request.method == 'POST':
        code = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit code
        request.session['email_change_code'] = code  # Store the code in the session
        email = request.user.email 

        # Send the code to the user's current email address
        subject = 'Email Verification Code'
        message = f'''
            Subject: {subject}

            Hello {email},

            You have initiated a request to change your email address. To complete this process, please use the following verification code:

            Verification Code: {code}

            Please enter this code on the verification page to confirm your email address change. If you did not initiate this change, please disregard this email.

            Thank you for using our service.

            Sincerely,
            PassVault 
        '''
        # Send the email with the verification code to the user's current email address
        send_mail(subject, message, 'your_email@example.com', [email], fail_silently=False)
        messages.success(request, 'An email with a verification code has been sent.')
        return redirect('verify_email_change')
    return render(request, 'email_change/init_email_change.html')

@login_required(login_url='login')
def verify_email_change(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('email_change_code')
        if entered_code == stored_code:
            # Code verification successful, allow the user to submit a new email
            return redirect('submit_new_email')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'email_change/verify_email_change.html')

@login_required(login_url='login')
def submit_new_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')

        # Update the user's email address in the database
        request.user.email = new_email
        request.user.save()

        # Clear the email change code from the session
        request.session.pop('email_change_code', None)

        messages.success(request, 'Your email address has been updated.')
        return redirect('index')

    return render(request, 'email_change/submit_new_email.html')