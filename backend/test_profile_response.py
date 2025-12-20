import os
import django
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

User = get_user_model()
try:
    admin_user = User.objects.get(username='admin')
except User.DoesNotExist:
    print("Admin user not found!")
    exit(1)

client = APIClient()
client.force_authenticate(user=admin_user)

response = client.get('/api/auth/profile/') 
if response.status_code == 404:
    response = client.get('/api/profile/')

print(f"Status: {response.status_code}")
print(f"Data: {response.data}")
