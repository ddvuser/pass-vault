from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from django.core import mail
import re

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_register(self):
        data = {
            'email': 'new@user.com',
            'password1': 'nby6_uy4Y,$OE%FCMKSJ',
            'password2': 'nby6_uy4Y,$OE%FCMKSJ',
        }
        # Register
        response = self.client.post(reverse('register'), data)

        # Get user
        User = get_user_model()
        user = User.objects.get(email='new@user.com')

        # Check if user was registered
        self.assertEqual(user.email, 'new@user.com')
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        reg_data = {
            'email': 'new@user.com',
            'password1': 'nby6_uy4Y,$OE%FCMKSJ',
            'password2': 'nby6_uy4Y,$OE%FCMKSJ',
        }
        # Register user
        self.client.post(reverse('register'), reg_data)

        log_data = {
            'email': 'new@user.com',
            'password': 'nby6_uy4Y,$OE%FCMKSJ', 
        }
        # Login user
        response = self.client.post(reverse('login'), log_data)

        # Check if user is logged in
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

class PasswordChangeTestCase(TestCase):

    def setUp(self):
        # Create user
        User = get_user_model()
        self.test_email = "test@user.com"
        self.test_password = 'nby6_uy4Y,$OE%FCMKSJ' 
        self.user = User.objects.create_user(email=self.test_email, password=self.test_password)

        self.client = Client()
        log_data = {
            'email': self.test_email,
            'password': self.test_password,
        }
        # Log in new user
        self.client.post(reverse('login'), log_data)

    def test_password_change(self):
        data = {
            'old_password': self.test_password,
            'new_password1': 'K242vb`e$4hF',
            'new_password2': 'K242vb`e$4hF'
        }
        # Change password
        response = self.client.post(reverse('change_password'), data)

        # Check if success
        self.assertEqual(response.status_code, 302)

class PasswordResetTestCase(TestCase):

    def setUp(self):
        # Create new user
        User = get_user_model()
        self.test_email = "test@user.com"
        self.test_password = 'nby6_uy4Y,$OE%FCMKSJ'
        self.user = User.objects.create_user(email=self.test_email, password=self.test_password)
        
        self.client = Client()
        self.new_password = 'H2r324~3r-#a'
        self.email = mail.outbox

    def test_password_reset_view(self):

        # Access password reset page
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset/password_reset.html')

        # Check password reset email
        response = self.client.post(reverse('password_reset'), {'email':'test@user.com'})
        self.assertEqual(len(self.email), 1)
        self.assertEqual(self.email[0].to, ['test@user.com'])
        self.assertEqual(response.status_code, 302)
        
    def test_password_reset_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset/password_reset_done.html')

    def test_password_confirm(self):
        response = self.client.post(reverse('password_reset'), {'email':'test@user.com'})
        self.assertEqual(response.status_code, 302)

        email_body = self.email[0].body
        # extract password reset link from email
        link_pattern = r"(?P<url>https?://[^\s]+)"
        match = re.search(link_pattern, email_body)
        reset_link = match.group()
        data = {
            'new_password1': self.new_password,
            'new_password2': self.new_password
        }
        # Check if redirect after new password is set
        response = self.client.post(reset_link, data)
        self.assertEqual(response.status_code, 302)





