from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    CustomUser, Role, Permission, Department,
    UserProfile, UserActivity
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'role', 'department', 'is_active', 'is_staff'
    )
    list_filter = ('is_active', 'is_staff', 'role', 'department')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserProfileInline,)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Organization'), {
            'fields': ('role', 'department')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'role',
                'is_staff', 'is_active'
            ),
        }),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_permissions_display', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)
    
    def get_permissions_display(self, obj):
        return ", ".join([str(p) for p in obj.permissions.all()[:3]])
    get_permissions_display.short_description = 'Permissions'

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('module', 'action', 'description')
    list_filter = ('module', 'action')
    search_fields = ('description',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'parent', 'created_at')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    raw_id_fields = ('manager',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'action_type', 'action_detail',
        'ip_address', 'timestamp'
    )
    list_filter = ('action_type', 'timestamp')
    search_fields = ('user__email', 'action_detail')
    date_hierarchy = 'timestamp'
    readonly_fields = (
        'user', 'action_type', 'action_detail',
        'ip_address', 'user_agent', 'timestamp'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
