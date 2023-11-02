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
    path('profile/', views.profile, name='profile'),
    # CRUD item
    path('add-item/', views.add_item, name='add_item'),
    path('view-item/<int:id>/', views.view_item, name='view_item'),
    path('delete-item/<int:id>/', views.delete_item, name='delete_item'),
    path('edit-item/<int:id>/', views.edit_item, name='edit_item'),
    # CRUD Folder
    path('add-folder/', views.add_folder, name='add_folder'),
    path('view-folder/<str:name>/', views.view_folder, name='view_folder'),
    path('edit-folder/<str:name>/', views.edit_folder, name='edit_folder'),
    path('delete-folder/<str:name>/', views.delete_folder, name='delete_folder'),
    # Registration
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Password change
    path('change-password/', views.change_password, name='change_password'),
    # Email change
    path('init-email-change/', views.init_email_change, name='init_email_change'),
    path('verify-email-change/', views.verify_email_change, name='verify_email_change'),
    path('submit-new-email/', views.submit_new_email, name='submit_new_email'),
    # Password reset
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