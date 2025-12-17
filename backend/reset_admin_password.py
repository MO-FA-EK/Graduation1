import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print("✓ Admin password reset successfully!")
    print("  Username: admin")
    print("  Password: admin123")
except User.DoesNotExist:
    print("✗ Admin user does not exist")
