from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Entry, Folder

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AddItemForm(forms.ModelForm):
    name = forms.CharField(max_length=80, strip=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Entry
        fields = ['name', 'password', 'email', 'note', 'folder']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'password', 'email', 'note', 'folder']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'folder': forms.Select(attrs={'class': 'form-select'}),
        }

class AddFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name',]
    
    name = forms.CharField(max_length=80, strip=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class EditFolderForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name',]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
