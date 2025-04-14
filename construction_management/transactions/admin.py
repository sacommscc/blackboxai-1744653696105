from django.contrib import admin
from .models import (
    Project, ExpenseCategory, Department, FinancialTransaction,
    RecurringTransaction, TransactionAttachment
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'end_date', 'budget', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'location')
    date_hierarchy = 'start_date'

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'description')
    list_filter = ('parent',)
    search_fields = ('name', 'description')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'description')
    search_fields = ('name', 'description')

class TransactionAttachmentInline(admin.TabularInline):
    model = TransactionAttachment
    extra = 1

@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number', 'transaction_type', 'amount', 'date',
        'payment_method', 'project'
    )
    list_filter = (
        'transaction_type', 'payment_method', 'date',
        'project', 'department', 'category'
    )
    search_fields = ('reference_number', 'description', 'transaction_id')
    date_hierarchy = 'date'
    inlines = [TransactionAttachmentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'transaction_type', 'amount', 'date', 'description',
                'reference_number'
            )
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Categorization', {
            'fields': ('project', 'department', 'category')
        }),
        ('Related Records', {
            'fields': ('vendor_purchase', 'labour_payment')
        }),
    )

@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'amount', 'frequency',
        'start_date', 'next_due_date', 'is_active'
    )
    list_filter = ('frequency', 'is_active', 'vendor')
    search_fields = ('description', 'vendor__name')
    date_hierarchy = 'next_due_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'amount', 'frequency')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'next_due_date', 'is_active')
        }),
        ('Categorization', {
            'fields': ('vendor', 'category', 'project')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

@admin.register(TransactionAttachment)
class TransactionAttachmentAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'description', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('description', 'transaction__reference_number')
    date_hierarchy = 'uploaded_at'
