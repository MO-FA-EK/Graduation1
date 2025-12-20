import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
django.setup()

from marketplace.models import Project
from marketplace.serializers import ProjectSerializer

try:
    print("Fetching first project...")
    p = Project.objects.first()
    if p:
        print(f"Project found: {p.title}")
        print("Attempting serialization...")
        s = ProjectSerializer(p)
        print(s.data)
        print("Serialization successful.")
    else:
        print("No projects found to test.")

except Exception:
    traceback.print_exc()

print("\nChecking Project model fields:")
print([f.name for f in Project._meta.get_fields()])
