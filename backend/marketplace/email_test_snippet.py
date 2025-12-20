from django.conf import settings
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status

class ContactEmailTestCase(TestCase):
    def test_contact_us_sends_email(self):
        client = APIClient()
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Help Needed',
            'message': 'Please help me.'
        }
        
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = client.post('/api/contact/', data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Contact Us: Help Needed')
            self.assertIn('Please help me', mail.outbox[0].body)
            self.assertEqual(mail.outbox[0].to, ['softwjob@gmail.com'])
