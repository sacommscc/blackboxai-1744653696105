from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from vendors.models import Vendor, Purchase
from labour.models import Labourer, LabourPayment

class Project(models.Model):
    """Model for tracking different construction projects"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']

class ExpenseCategory(models.Model):
    """Model for categorizing expenses"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subcategories'
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Expense Categories'

class Department(models.Model):
    """Model for different departments in the organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class FinancialTransaction(models.Model):
    """Model for tracking all financial transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('easypaisa', 'Easypaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    description = models.TextField()
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
    reference_number = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique reference number for this transaction'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='transactions',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='transactions',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='transactions',
        null=True,
        blank=True
    )
    vendor_purchase = models.ForeignKey(
        Purchase,
        on_delete=models.PROTECT,
        related_name='financial_transactions',
        null=True,
        blank=True
    )
    labour_payment = models.ForeignKey(
        LabourPayment,
        on_delete=models.PROTECT,
        related_name='financial_transactions',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference_number}"

    class Meta:
        ordering = ['-date', '-created_at']

class RecurringTransaction(models.Model):
    """Model for setting up recurring transactions"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    description = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name='recurring_transactions',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='recurring_transactions'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='recurring_transactions',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - {self.frequency}"

    class Meta:
        ordering = ['next_due_date']

class TransactionAttachment(models.Model):
    """Model for storing attachments related to transactions"""
    transaction = models.ForeignKey(
        FinancialTransaction,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='transaction_attachments/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.transaction.reference_number}"

    class Meta:
        ordering = ['-uploaded_at']
