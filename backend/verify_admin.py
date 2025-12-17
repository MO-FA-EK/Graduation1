import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin user found: {admin.username}")
    print(f"  - is_superuser: {admin.is_superuser}")
    print(f"  - is_staff: {admin.is_staff}")
    print(f"  - is_active: {admin.is_active}")
    
    if not admin.is_superuser:
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        print("\n✓ Admin permissions fixed!")
    else:
        print("\n✓ Admin already has superuser permissions")
        
except User.DoesNotExist:
    print("✗ Admin user does not exist. Creating...")
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@softwjob.com',
        password='admin123'
    )
    print(f"✓ Admin user created: {admin.username}")
    print("  Username: admin")
    print("  Password: admin123")
