from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class MaterialType(models.Model):
    """Model for different types of materials vendors can supply"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Vendor(models.Model):
    """Model for storing vendor information"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    material_types = models.ManyToManyField(MaterialType, related_name='vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class VendorProduct(models.Model):
    """Model for products/services offered by vendors"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('m', 'Meter'),
        ('sqm', 'Square Meter'),
        ('unit', 'Unit'),
        ('bag', 'Bag'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    price_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.vendor.name}"
    
    class Meta:
        ordering = ['name']
        unique_together = ['vendor', 'name']

class Purchase(models.Model):
    """Model for tracking purchases from vendors"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('easypaisa', 'Easypaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='purchases')
    product = models.ForeignKey(VendorProduct, on_delete=models.PROTECT, related_name='purchases')
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Transaction ID for non-cash payments'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Override save to calculate total amount"""
        self.total_amount = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Purchase from {self.vendor.name} - {self.purchase_date}"
    
    class Meta:
        ordering = ['-purchase_date']

class Payment(models.Model):
    """Model for tracking payments made to vendors"""
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=10,
        choices=Purchase.PAYMENT_METHOD_CHOICES
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Transaction ID for non-cash payments'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of PKR {self.amount} for {self.purchase}"
    
    class Meta:
        ordering = ['-payment_date']
