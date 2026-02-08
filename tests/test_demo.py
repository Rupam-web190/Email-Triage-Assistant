import unittest
import json
import os
import sys
import io
from datetime import datetime

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import app

class TestDemoScenarios(unittest.TestCase):
    """
    High-priority test cases for demo video recording.
    Demonstrates core functionality, error handling, and performance.
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_health_check(self):
        """Verify server is running and healthy"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
        print("\n[PASS] Health Check: System Online")

    def test_02_upload_eml_success(self):
        """Demonstrate successful EML file upload and parsing"""
        eml_content = b"""From: boss@company.com
To: me@company.com
Subject: Urgent Project Update
Date: Wed, 12 Feb 2025 10:00:00 -0000

We need to finalize the Q1 report by Friday.
"""
        data = {
            'file': (io.BytesIO(eml_content), 'urgent_update.eml')
        }
        response = self.app.post('/triage', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['subject'], 'Urgent Project Update')
        self.assertIn('priority', result)
        print(f"\n[PASS] File Upload: Processed 'urgent_update.eml' -> Priority: {result.get('priority_score', 'N/A')}")

    def test_03_upload_invalid_file(self):
        """Demonstrate robust error handling for invalid files"""
        data = {
            'file': (io.BytesIO(b"malicious content"), 'virus.exe')
        }
        response = self.app.post('/triage', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertIn('error', result)
        print("\n[PASS] Security: Blocked invalid file type 'virus.exe'")

    def test_04_batch_processing(self):
        """Demonstrate high-volume batch processing capability"""
        response = self.app.post('/batch')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'completed')
        self.assertGreater(len(data['results']), 0)
        print(f"\n[PASS] Batch Process: Processed {len(data['results'])} threads in {data['time_taken']}s")

    def test_05_generate_reply(self):
        """Demonstrate AI auto-reply generation"""
        payload = {
            "thread": {
                "id": "123",
                "subject": "Meeting Request",
                "body": "Can we meet tomorrow at 10am?",
                "sender": "client@example.com"
            },
            "tone": "professional"
        }
        response = self.app.post('/reply', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('draft_reply', data)
        print("\n[PASS] AI Reply: Generated professional response")

    def test_06_analytics_dashboard(self):
        """Verify analytics data retrieval"""
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        print("\n[PASS] Analytics: Dashboard data loaded")

if __name__ == '__main__':
    unittest.main(verbosity=2)
