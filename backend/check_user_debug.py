import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

with open('debug_result_internal.txt', 'w', encoding='utf-8') as f:
    f.write(f"DTO Database Path: {settings.DATABASES['default']['NAME']}\n")
    f.write("-" * 50 + "\n")
    f.write(f"{'Username':<20} | {'Active':<10} | {'Superuser':<10} | {'Pwd Hash Start'}\n")
    f.write("-" * 50 + "\n")

    for u in User.objects.all():
        f.write(f"{u.username:<20} | {str(u.is_active):<10} | {str(u.is_superuser):<10} | {u.password[:15]}...\n")

    f.write("-" * 50 + "\n")

    if User.objects.filter(username='new_admin').exists():
        ua = User.objects.get(username='new_admin')
        f.write("Trying manual password check for 'new_admin' with 'admin123':\n")
        f.write(f"Check Result: {ua.check_password('admin123')}\n")
    else:
        f.write("'new_admin' NOT FOUND.\n")
