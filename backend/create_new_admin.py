import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

username = 'new_admin'
email = 'admin@example.com'
password = 'admin123'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✓ SUPERUSER CREATED SUCCESSFULLY!")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Login at: /login then go to /admin")
    else:
        print(f"⚠ User '{username}' already exists.")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print(f"✓ Password reset to '{password}' for existing user.")

except Exception as e:
    print(f"✗ Error: {e}")
