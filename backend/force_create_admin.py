import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()
from django.contrib.auth.models import User

try:
    if User.objects.filter(username='new_admin').exists():
        u = User.objects.get(username='new_admin')
        u.set_password('admin123')
        u.is_active = True
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print("Updated existing user 'new_admin' with password 'admin123'")
    else:
        User.objects.create_superuser('new_admin', 'admin@example.com', 'admin123')
        print("Created new superuser 'new_admin' with password 'admin123'")
except Exception as e:
    print(f"Error: {e}")
