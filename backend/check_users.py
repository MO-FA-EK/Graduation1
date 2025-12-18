import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Programmer

print(f"Total Users: {User.objects.count()}")

for user in User.objects.all():
    user_type = 'client'
    if user.is_superuser:
        user_type = 'admin'
    elif hasattr(user, 'programmer'):
        user_type = 'freelancer'
    
    print(f"ID: {user.id} | Username: {user.username} | Email: {user.email} | Type: {user_type} | Superuser: {user.is_superuser}")
