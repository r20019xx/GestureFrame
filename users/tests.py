from django.test import TestCase
from django.contrib.auth.models import User
from .models import Detail


class UserTestCase(TestCase):
    # Newly registed user test
    def setUp(self):
        User.objects.create(username="victor", email="<EMAIL>", password="<PASSWORD>")

    def test_user_in_session(self):
        user = User.objects.get(username="victor")
        self.assertEqual(user.username, "victor")
        self.assertEqual(user.email, "<EMAIL>")
        self.assertEqual(user.password, "<PASSWORD>")
        self.assertEqual(user.detail.role, "regular")
