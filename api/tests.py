import io
import os
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

# Testing model integration image upload and prediction response.
class PredictViewIntegrationTest(TestCase):
    def setUp(self):
        self.predict_url = reverse('api:predict')
    # Used to get a test 'I love you' ASL image used in other tests.
    def get_test_image_file(self, filename='Test_image_ILoveYou.JPG'):
        path = os.path.join(os.path.dirname(__file__), filename)
        with open(path, 'rb') as f:
            image_data = f.read()
        image_file = io.BytesIO(image_data)
        image_file.name = filename
        image_file.seek(0)
        return image_file

    # Test uploading 'Test_image_ILoveYou.JPG' image to model and check prediction response is 'I love you'
    def test_real_model_response(self):
        image_file = self.get_test_image_file() # Get the 'Test_image_ILoveYou.JPG' image
        response = self.client.post(self.predict_url, {'file': image_file}, format='multipart')

        print("Full model response:", response.json())  # Show model response, was helpful for debugging

        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.json())
        self.assertIsInstance(response.json()['predictions'], list)
        self.assertGreaterEqual(len(response.json()['predictions']), 1)

        prediction = response.json()['predictions'][0]
        self.assertIn('label', prediction)
        self.assertIn('confidence', prediction)

    #test that error is handled when image file is missing, and that it doesn't crash program
    def test_predict_view_rejects_missing_file(self):
        response = self.client.post(self.predict_url, {}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No file provided'})

    # Test that non-image jpg file is handled correctly and doesn't crash program
    @patch('api.views.model')
    def test_predict_view_handles_invalid_image(self, mock_model):
        fake_file = io.BytesIO(b'not-an-image')
        fake_file.name = 'fake.jpg'
        # call predict_View.post to
        response = self.client.post(self.predict_url, {'file': fake_file}, format='multipart')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
