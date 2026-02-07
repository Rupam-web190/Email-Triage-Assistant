import requests
import json
import os

# Create a dummy EML file content
eml_content = """From: sender@example.com
To: receiver@example.com
Subject: Test Email
Date: Wed, 12 Feb 2025 10:00:00 -0000

This is a test email body.
"""

url = 'http://127.0.0.1:5000/triage'

payload = {
    "body": eml_content,
    "subject": "Test Email",
    "sender": "Unknown <sender@example.com>"
}

headers = {'Content-Type': 'application/json'}

try:
    print(f"Sending POST request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
