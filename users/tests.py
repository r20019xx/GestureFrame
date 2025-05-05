from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')

    def test_profile_view_exists_at_correct_url(self):
        url = reverse('users:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        url = reverse('users:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/user/profile.html')

    def test_profile_view_passes_correct_user_context(self):
        url = reverse('users:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.context['user'], self.user)

    def test_profile_view_returns_404_for_nonexistent_user(self):
        url = reverse('users:profile', kwargs={'username': 'nonexistentuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.register_url = reverse('users:register')

    def test_register_view_get_displays_form(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user/register.html')
        self.assertNotIn('username', response.context)
        self.assertNotIn('email', response.context)


    def test_register_view_post_creates_new_user(self):
        post_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.register_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertTrue(new_user.check_password('password123'))
        self.assertRedirects(response, reverse('users:profile', kwargs={'username': 'newuser'}))
        self.assertEqual(self.client.session['username'], 'newuser')
        self.assertEqual(self.client.session['role'], 'user')
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'User created successfully with the username: newuser')

    def test_register_view_post_renders_form_with_username_error(self):
        User.objects.create_user(username='existinguser', email='test@example.com', password='password')
        post_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.register_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user/register.html')
        self.assertEqual(response.context['username'], 'existinguser')
        self.assertEqual(response.context['email'], 'new@example.com')
        self.assertTrue(response.context['username_error'])
        self.assertFalse(response.context['email_error'])
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("The username 'existinguser' is already taken.", str(messages_list[0]))

    def test_register_view_post_renders_form_with_email_error(self):
        User.objects.create_user(username='newuser', email='existing@example.com', password='password')
        post_data = {
            'username': 'anotheruser',
            'email': 'existing@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.register_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user/register.html')
        self.assertEqual(response.context['username'], 'anotheruser')
        self.assertEqual(response.context['email'], 'existing@example.com')
        self.assertFalse(response.context['username_error'])
        self.assertTrue(response.context['email_error'])
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("The email 'existing@example.com' is already registered.", str(messages_list[0]))

    @patch('django.contrib.auth.models.User.objects.create_user', side_effect=Exception("Simulated error"))
    def test_register_view_post_handles_unexpected_error(self, mock_create_user):
        post_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password'
        }
        response = self.client.post(self.register_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user/register.html')
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'An unexpected error occurred. Please try again.')
        mock_create_user.assert_called_once_with('test', 'test@test.com', 'password')

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_login_view_post_logs_in_user_with_correct_credentials(self):
        post_data = {
            'username': 'testuser',
            'pw': 'testpassword'
        }
        response = self.client.post(self.login_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page:homeview'))
        self.assertEqual(self.client.session['username'], 'testuser')
        # Assuming you have a UserDetail model with a 'role' field
        self.client.session['role'] = getattr(self.user, 'detail', None).role if hasattr(self.user, 'detail') else None
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'You have logged in successfully!')

    def test_login_view_post_displays_error_with_incorrect_credentials(self):
        post_data = {
            'username': 'testuser',
            'pw': 'wrongpassword'
        }
        response = self.client.post(self.login_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page:homeview'))
        self.assertNotIn('username', self.client.session)
        self.assertNotIn('role', self.client.session)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Invalid username or password')

    def test_login_view_post_displays_error_with_nonexistent_user(self):
        post_data = {
            'username': 'nonexistentuser',
            'pw': 'anypassword'
        }
        response = self.client.post(self.login_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page:homeview'))
        self.assertNotIn('username', self.client.session)
        self.assertNotIn('role', self.client.session)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Invalid username or password')


class LogoutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.logout_url = reverse('users:logout')

    def test_logout_view_removes_username_and_role_from_session(self):
        session = self.client.session
        session['username'] = 'loggedinusertest'
        session['role'] = 'testrole'
        session.save()
        self.client.cookies['sessionid'] = session.session_key
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page:homeview'))
        self.assertNotIn('username', self.client.session)
        self.assertNotIn('role', self.client.session)