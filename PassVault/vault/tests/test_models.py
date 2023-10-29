from django.test import TestCase
from vault.models import CustomUser, Folder, Entry
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@user.com", password="foo")
        self.assertEqual(user.email, "test@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)

class EntryTestCase(TestCase):

    def test_entry_creation(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@user.com", password="foo")
        folder_data = {
            'user': user,
            'name': 'Test Folder'
        } 
        folder = Folder.objects.create(**folder_data)

        entry_data = {
            'user': user,
            'name': 'Test Entry',
            'folder': folder
        }
        entry = Entry.objects.create(**entry_data)
        self.assertEqual(folder.user, user)
        self.assertEqual(entry.folder, folder)
        self.assertEqual(entry.user, user)
