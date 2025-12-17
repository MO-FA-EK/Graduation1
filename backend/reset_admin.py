import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if User.objects.filter(username='admin').exists():
        u = User.objects.get(username='admin')
        print(f"Updating existing admin user (ID: {u.id})")
    else:
        u = User(username='admin')
        print("Creating new admin user")

    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.email = 'admin@softwjob.com'
    u.save()
    print("SUCCESS: Admin password reset to 'admin123'")

except Exception as e:
    print(f"ERROR: {e}")
