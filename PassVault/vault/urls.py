from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email'),
    path('password-reset/', 
         PasswordResetView.as_view(template_name='password_reset/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]