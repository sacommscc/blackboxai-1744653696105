from django.core.management.base import BaseCommand
from users.models import Role, Permission

class Command(BaseCommand):
    help = 'Create initial roles and permissions'

    def handle(self, *args, **kwargs):
        # Create permissions for each module
        modules = ['vendors', 'labour', 'transactions', 'reporting', 'users']
        actions = ['view', 'add', 'edit', 'delete', 'approve']
        
        permissions = []
        for module in modules:
            for action in actions:
                permission, created = Permission.objects.get_or_create(
                    module=module,
                    action=action,
                    description=f'{action.capitalize()} {module}'
                )
                permissions.append(permission)

        # Create admin role with all permissions
        admin_role, created = Role.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Administrator with full access'
            }
        )
        admin_role.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created roles and permissions'))
