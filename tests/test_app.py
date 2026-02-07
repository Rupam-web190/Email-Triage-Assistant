import unittest
import os
import sys
import io
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import app

class TestEmailTriage(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_no_file(self):
        response = self.app.post('/triage')
        self.assertEqual(response.status_code, 415) # Expect 415 Unsupported Media Type if no content-type/file

    def test_upload_invalid_extension(self):
        data = {
            'file': (io.BytesIO(b"dummy content"), 'test.txt')
        }
        response = self.app.post('/triage', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid file type', response.get_json()['error'])

    def test_upload_malicious_script(self):
        # Create a mock EML with a script tag
        eml_content = (
            b"Subject: Test Security\n"
            b"From: hacker@bad.com\n"
            b"Content-Type: text/html\n\n"
            b"<html><body><p>Safe text</p><script>alert('XSS')</script></body></html>"
        )
        data = {
            'file': (io.BytesIO(eml_content), 'attack.eml')
        }
        response = self.app.post('/triage', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        
        # Verify script is stripped
        response_data = response.get_json()
        # The engine returns 'summary' instead of 'body'
        self.assertIn('Safe text', response_data['summary'])
        self.assertNotIn('alert', response_data['summary'])
        self.assertNotIn('<script>', response_data['summary'])

    def test_pagination(self):
        # Test Page 1
        res1 = self.app.get('/threads?page=1&limit=5')
        self.assertEqual(res1.status_code, 200)
        data1 = res1.get_json()
        self.assertEqual(len(data1), 5)

        # Test Page 2
        res2 = self.app.get('/threads?page=2&limit=5')
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertEqual(len(data2), 5)

        # Ensure content is different (mock data relies on index)
        self.assertNotEqual(data1[0]['id'], data2[0]['id'])

if __name__ == '__main__':
    unittest.main()