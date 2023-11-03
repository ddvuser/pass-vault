from django.test import SimpleTestCase
from ..crypt_util import encrypt, decrypt

class CryptUtilTestCase(SimpleTestCase):

    def test_encrypt_decrypt(self):
        encryption_key = "my_secret_key"
        raw_str = "my_secret_password"

        # Encrypt the string
        encrypted_str = encrypt(raw_str, encryption_key)

        # Check if the encryption result is not the same as the raw string
        self.assertNotEqual(encrypted_str, raw_str)

        # Decrypt the string
        decrypted_str = decrypt(encrypted_str, encryption_key)

        # Check if the decrypted string matches the original raw string
        self.assertEqual(decrypted_str, raw_str)

    def test_bad_signature(self):
        encryption_key = "my_secret_key"
        raw_str = "my_secret_password"
        wrong_key = "wrong_key"

        # Encrypt the string
        encrypted_str = encrypt(raw_str, encryption_key)

        # Attempt to decrypt with the wrong key
        with self.assertRaises(ValueError):
            decrypt(encrypted_str, wrong_key)

    def test_different_keys(self):
        encryption_key1 = "key1"
        encryption_key2 = "key2"
        raw_str = "my_secret_password"

        # Encrypt the string with the first key
        encrypted_str = encrypt(raw_str, encryption_key1)

        # Attempt to decrypt with the second key
        with self.assertRaises(ValueError):
            decrypt(encrypted_str, encryption_key2)

    def test_empty_string(self):
        encryption_key = "my_secret_key"
        raw_str = ""

        # Encrypt the empty string
        encrypted_str = encrypt(raw_str, encryption_key)

        # Decrypt the empty string
        decrypted_str = decrypt(encrypted_str, encryption_key)

        # Check if the decrypted empty string matches the original empty string
        self.assertEqual(decrypted_str, raw_str)
