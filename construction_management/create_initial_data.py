import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_management.settings')
    django.setup()

def create_initial_data():
    from users.models import Role, Permission, CustomUser

    # Create admin role if it doesn't exist
    admin_role, created = Role.objects.get_or_create(
        name='admin',
        defaults={
            'description': 'Administrator with full system access'
        }
    )
    if created:
        print('Admin role created successfully')
    else:
        print('Admin role already exists')

    # Create permissions for each module and action
    modules = ['vendors', 'labour', 'transactions', 'reporting', 'users']
    actions = ['view', 'add', 'edit', 'delete', 'approve']

    for module in modules:
        for action in actions:
            permission, created = Permission.objects.get_or_create(
                module=module,
                action=action,
                defaults={
                    'description': f'{action.title()} {module}'
                }
            )
            if created:
                print(f'Created permission: {permission}')
            admin_role.permissions.add(permission)

    # Create superuser if it doesn't exist
    if not CustomUser.objects.filter(email='admin@example.com').exists():
        CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role=admin_role
        )
        print('Superuser created successfully')
    else:
        print('Superuser already exists')

if __name__ == '__main__':
    setup_django()
    create_initial_data()
