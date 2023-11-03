from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm, AddItemForm, EditItemForm, AddFolderForm, EditFolderForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from .models import Folder, Entry
import random
import string
from .crypt_util import encrypt, decrypt
import os

@login_required(login_url='login')
def index(request):
    folders = Folder.objects.filter(user=request.user)
    entries = Entry.objects.filter(user=request.user)
    return render(request, 'index.html', {'entries':entries, 'folders': folders})

@login_required(login_url='login')
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user

            # Create a new Entry instance and associate it with the user
            entry = form.save(commit=False)
            entry.user = user
            # Encrypt password and email before saving it
            if entry.password != "":
                entry.password = encrypt(entry.password, os.environ.get('SECRET_KEY'))
            if entry.email != "":
                entry.email = encrypt(entry.email, os.environ.get('SECRET_KEY'))
            entry.save()
            messages.success(request, 'Entry added.')
            return redirect('index')
        else:
            return redirect('add_item')
    else:
        form = AddItemForm()
    return render(request, 'item/add_item.html', {'form':form})
    
@login_required(login_url='login')
def delete_item(request, id):
    entry = get_object_or_404(Entry, user=request.user, id=id)
    if request.method == 'POST':
        entry.delete()
        return redirect('index')
    else:
        # confirm delete
        return render(request, 'item/delete_item_confirm.html', {'item':entry})

@login_required(login_url='login')
def edit_item(request, id):
    item = get_object_or_404(Entry, user=request.user, id=id)
    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            entry = form.save(commit=False)

            # Encrypt the password and email before saving it
            if entry.password != "":
                entry.password = encrypt(entry.password, os.environ.get('SECRET_KEY'))
            if entry.email != "":
                entry.email = encrypt(entry.email, os.environ.get('SECRET_KEY'))
            entry.save()
            return redirect('index')
    else:
        # Decrypt password and email before rendering the view
        if item.password != "":
            item.password = decrypt(item.password, os.environ.get('SECRET_KEY'))
        if item.email != "":
            item.email = decrypt(item.email, os.environ.get('SECRET_KEY'))
        form = EditItemForm(instance=item)  # Prepopulate the form with item's data

    return render(request, 'item/edit_item.html', {'form': form})

@login_required(login_url='login')
def view_item(request, id):
    if request.method == 'GET':
        item = get_object_or_404(Entry, user=request.user, id=id)
        if item.user == request.user:
            # Decrypt password and email before rendering the view
            if item.password != "":
                item.password = decrypt(item.password, os.environ.get('SECRET_KEY'))
            if item.email != "":
                item.email = decrypt(item.email, os.environ.get('SECRET_KEY'))
            return render(request, 'item/view_item.html', {'item':item})
        else:
            return HttpResponseNotFound('Item not found')
    else:
        return HttpResponseBadRequest('Ivalid Request.')
    
@login_required(login_url='login')
def add_folder(request):
    if request.method == 'POST':
        form = AddFolderForm(request.POST)
        if form.is_valid():
            # Get the currently logged-in user
            user = request.user

            # Create a new Entry instance and associate it with the user
            folder = form.save(commit=False)
            folder.user = user
            folder.save()
            messages.success(request, 'Folder added.')
            return redirect('index')
        else:
            return redirect('add_folder')
    else:
        form = AddFolderForm()
    return render(request, 'folder/add_folder.html', {'form':form})

@login_required(login_url='login')
def view_folder(request, name):
    if request.method == 'GET':
        folder = get_object_or_404(Folder, user=request.user, name=name)
        items = Entry.objects.filter(user=request.user, folder=folder)
        return render(request, 'folder/view_folder.html', {'items':items, 'folder':folder.name})
    else:
        return HttpResponseBadRequest('Invalid Request.')
    
@login_required(login_url='login')
def edit_folder(request, name):
    folder = get_object_or_404(Folder, user=request.user, name=name)
    if request.method == 'POST':
        form = EditFolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditFolderForm(instance=folder)  # Prepopulate the form with item's data
    return render(request, 'folder/edit_folder.html', {'form': form})

@login_required(login_url='login')
def delete_folder(request, name):
    folder = get_object_or_404(Folder, user=request.user, name=name)
    if request.method == 'POST':
        folder.delete()
        return redirect('index')
    else:
        # confirm delete
        return render(request, 'folder/delete_folder_confirm.html', {'folder':folder.name})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully registered.')
            return redirect('login')
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
                return redirect('profile')
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
            return redirect('profile')
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
        return redirect('profile')

    return render(request, 'email_change/submit_new_email.html')