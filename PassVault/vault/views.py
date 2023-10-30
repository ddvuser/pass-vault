from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

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
            error_messages = [error for field, error in form.errors.items()]
            for error in error_messages:
                messages.error(request, error) 
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

def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('index')
        else:
            error_messages = [error for field, error in form.errors.items()]
            for error in error_messages:
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form':form})