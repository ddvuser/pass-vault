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