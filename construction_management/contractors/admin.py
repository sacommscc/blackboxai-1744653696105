from django.contrib import admin
from .models import Contractor, ContractorPayment

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'specialization', 'phone', 'is_active')
    list_filter = ('is_active', 'specialization')
    search_fields = ('name', 'company_name', 'contact_person', 'phone', 'email')
    filter_horizontal = ('projects',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'company_name', 'specialization', 'rate_per_day')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'phone', 'email', 'address')
        }),
        ('Project Details', {
            'fields': ('projects', 'is_active')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContractorPayment)
class ContractorPaymentAdmin(admin.ModelAdmin):
    list_display = ('contractor', 'project', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date', 'project')
    search_fields = ('contractor__name', 'project__name', 'transaction_id')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('contractor', 'project', 'amount', 'payment_date')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'transaction_id', 'description')
        }),
        ('System Fields', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
