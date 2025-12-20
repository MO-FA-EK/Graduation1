import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()
from django.contrib.auth.models import User
try:
    u = User.objects.get(username='admin')
    print(f"User: {u.username}")
    print(f"Is Superuser: {u.is_superuser}")
    print(f"Is Staff: {u.is_staff}")
    print(f"Password Valid: {u.check_password('admin123')}")
except User.DoesNotExist:
    print("User 'admin' not found!")
