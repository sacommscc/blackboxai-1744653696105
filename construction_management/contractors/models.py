from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from transactions.models import Project

class Contractor(models.Model):
    """Model for managing contractors"""
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    specialization = models.CharField(max_length=200)
    rate_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Daily rate in PKR'
    )
    projects = models.ManyToManyField(
        Project,
        related_name='contractors',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

    class Meta:
        ordering = ['name']

class ContractorPayment(models.Model):
    """Model for tracking payments made to contractors"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('easypaisa', 'Easypaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
    ]

    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='contractor_payments'
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
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment to {self.contractor.name} - {self.payment_date}"

    class Meta:
        ordering = ['-payment_date']
