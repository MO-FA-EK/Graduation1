from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Programmer, Project, Review
from rest_framework.test import APIClient

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

class RatingAuthorizationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(username='client2', password='password')
        self.freelancer_user = User.objects.create_user(username='freelancer2', password='password')
        self.client.force_authenticate(user=self.client_user)

        self.programmer = Programmer.objects.create(
            user=self.freelancer_user,
            name='Freelancer 2',
            hourly_rate=60.00
        )

    def test_can_rate_completed_project(self):
        Project.objects.create(
            client=self.client_user,
            freelancer=self.programmer,
            status='completed',
            title='Completed Project'
        )
        response = self.client.post(f'/api/marketplace/rate/{self.programmer.id}/', {'rating': 5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(client=self.client_user, programmer=self.programmer).exists())

    def test_cannot_rate_active_project(self):
        Project.objects.create(
            client=self.client_user,
            freelancer=self.programmer,
            status='active',
            title='Active Project'
        )
        response = self.client.post(f'/api/marketplace/rate/{self.programmer.id}/', {'rating': 5})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Review.objects.filter(client=self.client_user, programmer=self.programmer).exists())

    def test_cannot_rate_no_project(self):
        response = self.client.post(f'/api/marketplace/rate/{self.programmer.id}/', {'rating': 5})
        self.assertEqual(response.status_code, 403)

    def test_cannot_rate_other_freelancer(self):
        other_freelancer_user = User.objects.create_user(username='other_freelancer', password='password')
        other_programmer = Programmer.objects.create(user=other_freelancer_user, name='Other', hourly_rate=40)
        
        Project.objects.create(
            client=self.client_user,
            freelancer=self.programmer,
            status='completed'
        )
        
        response = self.client.post(f'/api/marketplace/rate/{other_programmer.id}/', {'rating': 5})
        self.assertEqual(response.status_code, 403)

class ContactClickTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.freelancer_user = User.objects.create_user(username='freelancer_click', password='password')
        self.programmer = Programmer.objects.create(user=self.freelancer_user, name='Freelancer Click', hourly_rate=50)
        
        self.client_user1 = User.objects.create_user(username='client_click1', password='password')
        self.client_user2 = User.objects.create_user(username='client_click2', password='password')

    def test_owner_click_ignored(self):
        self.client.force_authenticate(user=self.freelancer_user)
        response = self.client.post(f'/api/marketplace/contact_click/{self.programmer.id}/')
        
        self.programmer.refresh_from_db()
        self.assertEqual(self.programmer.contact_clicks, 0)
        self.assertEqual(response.data['message'], 'Owner click ignored')

    def test_client_click_counts_once(self):
        self.client.force_authenticate(user=self.client_user1)
        
        response = self.client.post(f'/api/marketplace/contact_click/{self.programmer.id}/')
        self.programmer.refresh_from_db()
        self.assertEqual(self.programmer.contact_clicks, 1)
        
        response = self.client.post(f'/api/marketplace/contact_click/{self.programmer.id}/')
        self.programmer.refresh_from_db()
        self.assertEqual(self.programmer.contact_clicks, 1) 
        self.assertEqual(response.data['message'], 'Click already counted')

    def test_multiple_clients(self):
        self.client.force_authenticate(user=self.client_user1)
        self.client.post(f'/api/marketplace/contact_click/{self.programmer.id}/')
        
        self.client.force_authenticate(user=self.client_user2)
        self.client.post(f'/api/marketplace/contact_click/{self.programmer.id}/')
        
        self.programmer.refresh_from_db()
        self.assertEqual(self.programmer.contact_clicks, 2)

class AdminRestrictionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@test.com', password='password')
        self.freelancer_user = User.objects.create_user(username='freelancer_admin_test', password='password')
        self.programmer = Programmer.objects.create(user=self.freelancer_user, name='Freelancer Admin Test', hourly_rate=50)

    def test_admin_cannot_create_project(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'Admin Project',
            'description': 'Should fail',
            'amount': 50
        }
        response = self.client.post(f'/api/marketplace/projects/create/{self.programmer.id}/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error'], 'Admins cannot create projects.')
