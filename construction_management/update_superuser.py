import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_management.settings')
    django.setup()

def update_superuser():
    from users.models import Role, CustomUser
    
    # Get admin role
    admin_role = Role.objects.get(name='admin')
    
    # Update superuser
    superuser = CustomUser.objects.get(email='admin@example.com')
    superuser.role = admin_role
    superuser.save()
    print('Superuser updated with admin role')

if __name__ == '__main__':
    setup_django()
    update_superuser()
