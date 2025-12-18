from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Programmer, Project

User = get_user_model()

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='password')
        self.freelancer_user = User.objects.create_user(username='freelancer', password='password')
        
        self.programmer = Programmer.objects.create(
            user=self.freelancer_user,
            name='Freelancer',
            hourly_rate=50.00,
            balance=0.00
        )
        
        self.project = Project.objects.create(
            client=self.client_user,
            freelancer=self.programmer,
            title='Test Project',
            amount=100.00,
            status='pending',
            is_paid=False
        )

    def test_balance_defaults_to_zero(self):
        self.assertEqual(self.programmer.balance, 0.00)

    def test_payment_updates_balance(self):
       
        self.project.is_paid = True
        self.project.status = 'active'
        self.project.save()
        
        freelancer = self.project.freelancer
        freelancer.balance += self.project.amount
        freelancer.save()
        
        self.programmer.refresh_from_db()
        self.assertEqual(self.programmer.balance, 100.00)
        self.assertEqual(self.project.status, 'active')
        self.assertTrue(self.project.is_paid)

    def test_get_absolute_url(self):
        self.assertEqual(self.programmer.get_absolute_url(), f"/freelancer/{self.programmer.id}")
