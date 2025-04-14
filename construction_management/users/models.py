from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user model manager for handling email as the unique identifier"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Get or create admin role
        from users.models import Role
        admin_role = Role.objects.get(name='admin')
        extra_fields['role'] = admin_role

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom User model with email as the unique identifier"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        related_name='users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Role(models.Model):
    """Model for defining user roles"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
        ('supervisor', 'Supervisor'),
        ('staff', 'Staff'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField()
    permissions = models.ManyToManyField(
        'Permission',
        related_name='roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ['name']

class Permission(models.Model):
    """Model for defining granular permissions"""
    MODULE_CHOICES = [
        ('vendors', 'Vendor Management'),
        ('labour', 'Labour Management'),
        ('transactions', 'Financial Transactions'),
        ('reporting', 'Reporting & Analytics'),
        ('users', 'User Management'),
    ]

    ACTION_CHOICES = [
        ('view', 'View'),
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
    ]

    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_module_display()} - {self.get_action_display()}"

    class Meta:
        unique_together = ['module', 'action']
        ordering = ['module', 'action']

class Department(models.Model):
    """Model for organizing users into departments"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subdepartments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class UserProfile(models.Model):
    """Model for additional user profile information"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    joining_date = models.DateField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    preferences = models.JSONField(
        default=dict,
        help_text='User preferences and settings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"

class UserActivity(models.Model):
    """Model for tracking user activities"""
    ACTION_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_detail = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action_type} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'
