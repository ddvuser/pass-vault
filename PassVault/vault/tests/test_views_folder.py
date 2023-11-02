from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Folder

class FolderViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@user.com',
            password='testpassword'
        )
        self.client.login(email='test@user.com', password='testpassword')
        self.folder = Folder.objects.create(user=self.user, name='Test Folder')

    def test_add_folder_view(self):
        data = {
            'name': 'New Folder',
        }
        response = self.client.post(reverse('add_folder'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful folder addition
        self.assertTrue(Folder.objects.filter(name='New Folder').exists())

    def test_length_exceed(self):
        # Test name field length exceeding
        response = self.client.post(reverse('add_folder'), {'name': 'New2 Folder'*15})
        self.assertFalse(Folder.objects.filter(name='New Folder'*10).exists())
        self.assertEqual(response.status_code, 302)

    def test_view_folder_view(self):
        response = self.client.get(reverse('view_folder', args=[self.folder.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Folder')  # Check if folder name is in the response

    def test_edit_folder_view(self):
        response = self.client.get(reverse('edit_folder', args=[self.folder.name]))
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Edited Folder',
        }
        response = self.client.post(reverse('edit_folder', args=[self.folder.name]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful folder edit
        self.assertTrue(Folder.objects.filter(name='Edited Folder').exists())

    def test_delete_folder_view(self):
        response = self.client.get(reverse('delete_folder', args=[self.folder.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('delete_folder', args=[self.folder.name]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful folder deletion
        self.assertFalse(Folder.objects.filter(name='Test Folder').exists())
