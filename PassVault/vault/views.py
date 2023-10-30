from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm, EmailChangeForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

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
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email address has been updated.')
            return redirect('index')
        else:
            display_error_message(request, form.errors)
    else:
        form = EmailChangeForm(instance=request.user)

    return render(request, 'change_email.html', {'form': form})