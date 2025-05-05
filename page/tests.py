import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from page.models import comments


class HomeViewTest(TestCase):
    def test_home_view_renders_correct_template(self):
        response = self.client.get(reverse('page:homeview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/index.html')


class AboutViewTest(TestCase):
    def test_about_view_renders_correct_template(self):
        response = self.client.get(reverse('page:aboutview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/about.html')


class FeedbackViewTest(TestCase):
    def setUp(self):
        comments.objects.create(user='testuser1', date=datetime.datetime.now(), comment='Comment 1')
        comments.objects.create(user='testuser2', date=datetime.datetime.now(), comment='Comment 2')

    def test_feedback_view_renders_correct_template(self):
        response = self.client.get(reverse('page:feedbackview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/feedback.html')

    def test_feedback_view_passes_comments_list_in_context(self):
        response = self.client.get(reverse('page:feedbackview'))
        self.assertIn('commentsList', response.context)
        self.assertEqual(len(response.context['commentsList']), 2)
        self.assertEqual(response.context['commentsList'][0]['user'], 'testuser1')
        self.assertEqual(response.context['commentsList'][1]['comment'], 'Comment 2')


class CommentViewTest(TestCase):
    def setUp(self):
        self.comment_url = reverse('page:commentview')
        self.test_user = User.objects.create_user(username='testuser')

    def test_comment_view_rejects_non_ajax_requests(self):
        response = self.client.post(self.comment_url, {'comment_text': 'Test comment'})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid Ajax request'})

    def test_comment_view_rejects_non_post_ajax_requests(self):
        response = self.client.get(self.comment_url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid Ajax request'})

    @patch('page.models.comments.save', side_effect=Exception("Simulated database error"))
    def test_comment_view_handles_database_errors(self, mock_save):
        self.client.session['username'] = self.test_user.username
        session = self.client.session
        session.save()
        self.client.cookies['sessionid'] = session.session_key

        response = self.client.post(
            self.comment_url,
            {'comment_text': 'Comment that might cause error'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Simulated database error'})
        self.assertEqual(comments.objects.count(), 0)
        mock_save.assert_called_once()


class UploadViewTest(TestCase):
    def test_upload_view_renders_correct_template(self):
        response = self.client.get(reverse('page:uploadview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/upload.html')


class PrivacyPolicyViewTest(TestCase):
    def test_privacypolicy_view_renders_correct_template(self):
        response = self.client.get(reverse('page:privacypolicyview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/privacypolicy.html')


class FAQViewTest(TestCase):
    def test_faq_view_renders_correct_template(self):
        response = self.client.get(reverse('page:faqview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/faq.html')


class ContactViewTest(TestCase):
    def test_contact_view_renders_correct_template(self):
        response = self.client.get(reverse('page:contactview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/page_story/contact.html')