from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

class ReportTemplate(models.Model):
    """Model for storing report templates"""
    REPORT_TYPES = [
        ('vendor', 'Vendor Report'),
        ('labour', 'Labour Report'),
        ('financial', 'Financial Report'),
        ('project', 'Project Report'),
        ('tax', 'Tax Report'),
        ('custom', 'Custom Report'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    template_config = models.JSONField(
        help_text='JSON configuration for report layout and content'
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='report_templates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"

    class Meta:
        ordering = ['report_type', 'name']
        unique_together = ['name', 'report_type']

class SavedReport(models.Model):
    """Model for storing generated reports"""
    EXPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.PROTECT,
        related_name='saved_reports'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parameters = models.JSONField(
        help_text='Parameters used to generate the report'
    )
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    generated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='generated_reports'
    )
    export_format = models.CharField(max_length=10, choices=EXPORT_FORMATS)
    file = models.FileField(
        upload_to='reports/',
        null=True,
        blank=True,
        help_text='Generated report file'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_range_start} to {self.date_range_end}"

    class Meta:
        ordering = ['-created_at']

class TaxConfiguration(models.Model):
    """Model for storing tax-related configurations"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Tax rate as a percentage'
    )
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.tax_rate}%"

    class Meta:
        ordering = ['-effective_from']

class AnalyticsConfiguration(models.Model):
    """Model for configuring analytics dashboards"""
    CHART_TYPES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('table', 'Table View'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    chart_type = models.CharField(max_length=10, choices=CHART_TYPES)
    metrics = models.JSONField(
        help_text='JSON configuration for metrics to be displayed'
    )
    filters = models.JSONField(
        help_text='JSON configuration for available filters',
        null=True,
        blank=True
    )
    refresh_interval = models.IntegerField(
        help_text='Refresh interval in minutes',
        default=60
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='analytics_configs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_chart_type_display()}"

    class Meta:
        ordering = ['name']

class ScheduledReport(models.Model):
    """Model for scheduling automated report generation"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]

    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.PROTECT,
        related_name='scheduled_reports'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    parameters = models.JSONField(
        help_text='Parameters to be used for report generation'
    )
    recipients = models.ManyToManyField(
        User,
        related_name='subscribed_reports',
        help_text='Users who will receive the report'
    )
    export_format = models.CharField(
        max_length=10,
        choices=SavedReport.EXPORT_FORMATS
    )
    is_active = models.BooleanField(default=True)
    last_generated = models.DateTimeField(null=True, blank=True)
    next_generation = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_scheduled_reports'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.frequency}"

    class Meta:
        ordering = ['next_generation']
