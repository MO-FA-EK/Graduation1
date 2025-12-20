import sys
try:
    with open('crash_log.txt', 'w') as f:
        f.write('Start\n')
        try:
            import os
            import django
            f.write('Basic Imports done\n')
            
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmer_marketplace.settings')
            django.setup()
            f.write('Django Setup done\n')
            
            from django.contrib.auth.models import User
            count = User.objects.count()
            f.write(f'User count: {count}\n')
            
            if User.objects.filter(username='new_admin').exists():
                u = User.objects.get(username='new_admin')
                f.write(f"new_admin exists. Active: {u.is_active}, Super: {u.is_superuser}\n")
                u.set_password('admin123')
                u.save()
                f.write('Reset pwd to admin123\n')
            else:
                User.objects.create_superuser('new_admin', 'a@b.com', 'admin123')
                f.write('Created new_admin\n')
                
        except Exception as e:
            f.write(f'CRASH: {e}\n')
            import traceback
            traceback.print_exc(file=f)
except Exception as outer_e:
    print(f"FATAL: {outer_e}", file=sys.stderr)
