from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal

class LabourType(models.Model):
    """Model for different types of labour roles"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    base_daily_wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Base daily wage in PKR for this labour type'
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Skill(models.Model):
    """Model for specific skills that labourers may possess"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    labour_type = models.ForeignKey(
        LabourType,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    
    def __str__(self):
        return f"{self.name} ({self.labour_type.name})"
    
    class Meta:
        ordering = ['labour_type', 'name']

class Labourer(models.Model):
    """Model for storing labourer information"""
    # CNIC validator with format XXXXX-XXXXXXX-X
    cnic_validator = RegexValidator(
        regex=r'^\d{5}-\d{7}-\d{1}$',
        message='CNIC must be in the format XXXXX-XXXXXXX-X'
    )
    
    name = models.CharField(max_length=200)
    cnic = models.CharField(
        max_length=15,
        validators=[cnic_validator],
        unique=True,
        help_text='Format: XXXXX-XXXXXXX-X'
    )
    phone = models.CharField(max_length=20)
    address = models.TextField()
    labour_type = models.ForeignKey(
        LabourType,
        on_delete=models.PROTECT,
        related_name='labourers'
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='labourers',
        blank=True
    )
    daily_wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Daily wage in PKR'
    )
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.labour_type.name}"
    
    class Meta:
        ordering = ['name']

class WorkLog(models.Model):
    """Model for tracking labourer work hours and tasks"""
    labourer = models.ForeignKey(
        Labourer,
        on_delete=models.PROTECT,
        related_name='work_logs'
    )
    work_date = models.DateField()
    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Number of hours worked'
    )
    tasks_performed = models.ManyToManyField(
        Skill,
        related_name='work_logs',
        help_text='Skills/tasks performed during work'
    )
    description = models.TextField(
        blank=True,
        help_text='Additional details about work performed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def daily_wage_amount(self):
        """Calculate daily wage based on hours worked"""
        full_day_hours = Decimal('8.0')  # Standard work day
        wage_ratio = self.hours_worked / full_day_hours
        return self.labourer.daily_wage * wage_ratio
    
    def __str__(self):
        return f"{self.labourer.name} - {self.work_date}"
    
    class Meta:
        ordering = ['-work_date']
        unique_together = ['labourer', 'work_date']

class LabourPayment(models.Model):
    """Model for tracking payments made to labourers"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('easypaisa', 'Easypaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
    ]
    
    labourer = models.ForeignKey(
        Labourer,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    work_logs = models.ManyToManyField(
        WorkLog,
        related_name='payments',
        help_text='Work logs covered by this payment'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Transaction ID for non-cash payments'
    )
    bonus_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Additional bonus amount if any'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment to {self.labourer.name} - {self.payment_date}"
    
    class Meta:
        ordering = ['-payment_date']
