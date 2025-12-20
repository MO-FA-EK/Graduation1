import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

try:
    print("Running makemigrations...")
    call_command('makemigrations', 'marketplace')
    print("Running migrate...")
    call_command('migrate')
    print("Done.")
except Exception as e:
    print(f"Error: {e}")
