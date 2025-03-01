import unittest
import os
from email import policy
from email.parser import BytesParser
from io import BytesIO

# Assuming the EmailParser class is in a file named email_parser.py
from emailforensic import EmailParser

class TestEmailParser(unittest.TestCase):

    def setUp(self):
        # Create a sample email content for testing
        self.sample_email = b"""\
From: sender@example.com
To: recipient@example.com
Subject: Test Email
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"

This is a test email body.
"""
        # Write the sample email to a temporary file
        self.test_email_path = 'test_email.eml'
        with open(self.test_email_path, 'wb') as f:
            f.write(self.sample_email)

    def tearDown(self):
        # Remove the test email file after tests
        if os.path.exists(self.test_email_path):
            os.remove(self.test_email_path)

    def test_parse_email(self):
        parser = EmailParser(self.test_email_path)
        result = parser.parse_email()
        self.assertIn("Subject: Test Email", result)
        self.assertIn("From: sender@example.com", result)
        self.assertIn("To: recipient@example.com", result)
        self.assertIn("Content Type: text/plain", result)

    def test_get_email_body(self):
        parser = EmailParser(self.test_email_path)
        with open(self.test_email_path, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        body = parser.get_email_body(msg, 'plain')
        self.assertEqual(body, "This is a test email body.\n")

    def test_get_received_headers(self):
        parser = EmailParser(self.test_email_path)
        with open(self.test_email_path, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        received_headers = parser.get_received_headers(msg)
        self.assertEqual(received_headers, "N/A")  # No Received headers in sample email

    def test_get_authentication_results(self):
        parser = EmailParser(self.test_email_path)
        with open(self.test_email_path, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        auth_results = parser.get_authentication_results(msg)
        self.assertIn("SPF: N/A", auth_results)
        self.assertIn("DKIM: N/A", auth_results)
        self.assertIn("DMARC: N/A", auth_results)

    def test_get_attachments(self):
        parser = EmailParser(self.test_email_path)
        with open(self.test_email_path, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        attachments = parser.get_attachments(msg)
        self.assertEqual(attachments, "No Attachments")  # No attachments in sample email

if __name__ == '__main__':
    unittest.main()