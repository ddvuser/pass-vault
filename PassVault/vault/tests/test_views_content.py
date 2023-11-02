from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from ..models import Entry, Folder

class ItemViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@user.com',
            password='testpassword'
        )
        self.client.login(email='test@user.com', password='testpassword')
        self.folder = Folder.objects.create(user=self.user, name='Test Folder')
        self.item = Entry.objects.create(
            user=self.user,
            name='Test Item',
            folder=self.folder,
        )
    
    def test_add_item_view(self):
        response = self.client.get(reverse('add_item'))
        self.assertEqual(response.status_code, 200)

        data = {
            'name': 'New Item',
            'folder': self.folder.id,
        }
        response = self.client.post(reverse('add_item'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful item addition
        self.assertTrue(Entry.objects.filter(name='New Item').exists())

    def test_view_item_view(self):
        response = self.client.get(reverse('view_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')  # Check if item name is in the response

    def test_edit_item_view(self):
        response = self.client.get(reverse('edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Edited Item',
            'folder': self.folder.id,
        }
        response = self.client.post(reverse('edit_item', args=[self.item.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful item edit
        self.assertTrue(Entry.objects.filter(name='Edited Item').exists())

    def test_delete_item_view(self):
        response = self.client.get(reverse('delete_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('delete_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful item deletion
        self.assertFalse(Entry.objects.filter(name='Test Item').exists())       

class ItemViewsSecurityTestCase(TestCase):
    def setUp(self):
        # User 1
        self.user1 = get_user_model().objects.create_user(
            email='test1@user.com',
            password='password1'
        )
        self.client1 = Client()
        self.client1.login(email='test1@user.com', password='password1')

        # User 2
        self.user2 = get_user_model().objects.create_user(
            email='test2@user.com',
            password='password2'
        )
        self.client2 = Client()
        self.client2.login(email='test2@user.com', password='password2')

        # User 1's folder and item
        self.folder1 = Folder.objects.create(user=self.user1, name='User 1 Folder')
        self.item1 = Entry.objects.create(
            user=self.user1,
            name='User 1 Item',
            folder=self.folder1,
        )

        # User 2's folder and item
        self.folder2 = Folder.objects.create(user=self.user2, name='User 2 Folder')
        self.item2 = Entry.objects.create(
            user=self.user2,
            name='User 2 Item',
            folder=self.folder2,
        )

    def test_user_cannot_access_another_users_items(self):
        # User 1 trying to access User 2's item
        response = self.client1.get(reverse('view_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 404)

        # User 1 trying to edit User 2's item
        response = self.client1.get(reverse('edit_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 404)

        # User 1 trying to delete User 2's item
        response = self.client1.get(reverse('delete_item', args=[self.item2.id]))
        self.assertEqual(response.status_code, 404)