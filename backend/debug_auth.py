import os
import django
from django.conf import settings

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

username = 'admin'
password = 'admin123'

print(f"--- Debugging Auth for user: {username} ---")

# 1. Check if user exists
try:
    user = User.objects.get(username=username)
    print(f"User found: ID={user.id}, IsSuperuser={user.is_superuser}, IsActive={user.is_active}")
    print(f"Password set: {user.password[:20]}...")
except User.DoesNotExist:
    print("User 'admin' does NOT exist.")
    exit()

# 2. Check password directly
print(f"Checking password '{password}'...")
is_correct = user.check_password(password)
print(f"user.check_password('{password}') returned: {is_correct}")

# 3. Check authenticate()
print("Attempting to authenticate via Django auth backend...")
user_auth = authenticate(username=username, password=password)
if user_auth is not None:
    print("Authentication SUCCESSFUL.")
else:
    print("Authentication FAILED. (check_password was True? " + str(is_correct) + ")")
