from django.test import TestCase, Client
from accounts.models import User
import unittest
# Create your tests here.


# Tests for models

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_staff(email='suryaaddu@gmail.com', password='sur21997', username='surya')
        User.objects.create_superuser(email='kathi@gmail.com', password='kat21997', username='kathi')

    def test_user_permissions(self):
        surya = User.objects.get(email='suryaaddu@gmail.com')
        kathi = User.objects.get(email='kathi@gmail.com')
        self.assertEqual(surya.is_staff, True)
        self.assertEqual(surya.is_admin, False)
        self.assertEqual(surya.get_email, 'suryaaddu@gmail.com')
        self.assertEqual(kathi.is_staff, True)
        self.assertEqual(kathi.is_admin, True)
        self.assertEqual(kathi.get_email, 'kathi@gmail.com')






# Tests for views


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    def test_details(self):
        response = self.client.get('/accounts/signin')
        self.assertEqual(response.status_code, 200)

# Tests for forms