import os
import email
from email import policy
from email.parser import BytesParser
import glob
import random
from datetime import datetime, timedelta

class GmailParser:
    def __init__(self, test_cases_dir='../test_cases'):
        self.test_cases_dir = test_cases_dir
        self.service = None  # Placeholder for real Gmail API service

    def connect(self):
        """Simulate connection"""
        return True

    def fetch_threads(self, limit=50, offset=0):
        """
        Fetch threads from Gmail. 
        For this demo, we will read from test_cases folder or generate mock data.
        """
        threads = []
        
        # Try to read .eml files from test_cases
        eml_files = glob.glob(os.path.join(self.test_cases_dir, '*.eml'))
        
        if eml_files:
            for file_path in eml_files:
                with open(file_path, 'rb') as f:
                    msg = BytesParser(policy=policy.default).parse(f)
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    else:
                        body = msg.get_payload(decode=True).decode()

                    threads.append({
                        "id": os.path.basename(file_path).replace('.eml', ''),
                        "subject": msg['subject'],
                        "sender": msg['from'],
                        "date": msg['date'],
                        "snippet": body[:100] + "...",
                        "body": body,
                        "messages": [{"role": "user", "content": body}] # Simplified for triage
                    })
        
        # If we don't have enough files to meet the limit + offset, generate synthetic ones
        total_needed = offset + limit
        while len(threads) < total_needed:
            threads.append(self._generate_mock_thread(len(threads)))
            
        return threads[offset:offset+limit]

    def _generate_mock_thread(self, index):
        """Generate a synthetic email thread for volume testing"""
        senders = ["boss@company.com", "client@client.com", "newsletter@spam.com", "hr@company.com", "support@tool.io"]
        subjects = ["Urgent Update", "Meeting Request", "Weekly Newsletter", "Policy Change", "Ticket #1234"]
        
        sender = senders[index % len(senders)]
        subject = f"{subjects[index % len(subjects)]} - {index}"
        body = f"This is a simulated email body for thread {index}. It contains some text to simulate a real email conversation. We need to verify that the batch processing works correctly."
        
        return {
            "id": f"mock_thread_{index}",
            "subject": subject,
            "sender": sender,
            "date": (datetime.now() - timedelta(minutes=index*10)).strftime("%a, %d %b %Y %H:%M:%S"),
            "snippet": body[:50] + "...",
            "body": body,
            "messages": [{"role": "user", "content": body}]
        }
