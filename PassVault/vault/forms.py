from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Entry, Folder

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'password', 'email', 'note', 'folder']

    name = forms.CharField(max_length=80, strip=True)
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    note = forms.CharField(widget=forms.Textarea, required=False)
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False)