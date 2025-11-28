from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class ProgrammerAPITests(APITestCase):

    def setUp(self):
        # Sample programmer
        self.user = User.objects.create(
            name="Hamze",
            email="hamze@example.com",
            skills="Python, Django",
            category="Backend",
            experience_level="Senior",
            bio="Experienced backend developer."
        )
        self.list_url = reverse('programmer_list')

    def test_get_all_programmers(self):
        """✅ Test GET /api/programmers/"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data['results'][0])

    def test_create_programmer(self):
        """✅ Test POST /api/programmers/"""
        data = {
            "name": "Mohammed",
            "email": "mohammed@example.com",
            "skills": "HTML, CSS, JS",
            "category": "Frontend",
            "experience_level": "Junior",
            "bio": "Frontend developer specialized in UI/UX"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
