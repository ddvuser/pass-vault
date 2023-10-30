from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_register(self):
        data = {
            'email': 'new@user.com',
            'password1': 'nby6_uy4Y,$OE%FCMKSJ',
            'password2': 'nby6_uy4Y,$OE%FCMKSJ',
        }
        response = self.client.post(reverse('register'), data)

        # Check that the user was created
        User = get_user_model()
        user = User.objects.get(email='new@user.com')

        self.assertEqual(user.email, 'new@user.com')
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        # Register user
        reg_data = {
            'email': 'new@user.com',
            'password1': 'nby6_uy4Y,$OE%FCMKSJ',
            'password2': 'nby6_uy4Y,$OE%FCMKSJ',
        }
        self.client.post(reverse('register'), reg_data)

        # Login user
        log_data = {
            'email': 'new@user.com',
            'password': 'nby6_uy4Y,$OE%FCMKSJ', 
        }
        response = self.client.post(reverse('login'), log_data)

        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

class PasswordChangeTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.test_email = "test@user.com"
        self.test_password = 'nby6_uy4Y,$OE%FCMKSJ' 
        self.user = User.objects.create_user(email=self.test_email, password=self.test_password)

        self.client = Client()
        log_data = {
            'email': self.test_email,
            'password': self.test_password,
        }
        self.client.post(reverse('login'), log_data)

    def test_password_change(self):
        data = {
            'old_password': self.test_password,
            'new_password1': 'K242vb`e$4hF',
            'new_password2': 'K242vb`e$4hF'
        }
        response = self.client.post(reverse('change_password'), data)

        self.assertEqual(response.status_code, 302)

