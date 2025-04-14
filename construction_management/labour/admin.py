from django.contrib import admin
from .models import LabourType, Skill, Labourer, WorkLog, LabourPayment

@admin.register(LabourType)
class LabourTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_daily_wage')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'labour_type', 'description')
    list_filter = ('labour_type',)
    search_fields = ('name', 'description')

@admin.register(Labourer)
class LabourerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnic', 'phone', 'labour_type', 'daily_wage', 'is_active')
    list_filter = ('labour_type', 'is_active', 'joining_date')
    search_fields = ('name', 'cnic', 'phone')
    filter_horizontal = ('skills',)
    date_hierarchy = 'joining_date'
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'cnic', 'phone', 'address')
        }),
        ('Work Information', {
            'fields': ('labour_type', 'skills', 'daily_wage', 'joining_date', 'is_active')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('labourer', 'work_date', 'hours_worked', 'daily_wage_amount')
    list_filter = ('work_date', 'labourer__labour_type')
    search_fields = ('labourer__name', 'description')
    date_hierarchy = 'work_date'
    filter_horizontal = ('tasks_performed',)
    readonly_fields = ('daily_wage_amount',)

@admin.register(LabourPayment)
class LabourPaymentAdmin(admin.ModelAdmin):
    list_display = ('labourer', 'amount', 'payment_date', 'payment_method', 'bonus_amount')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('labourer__name', 'transaction_id')
    date_hierarchy = 'payment_date'
    filter_horizontal = ('work_logs',)
    fieldsets = (
        ('Payment Information', {
            'fields': ('labourer', 'amount', 'payment_date', 'payment_method')
        }),
        ('Additional Details', {
            'fields': ('transaction_id', 'bonus_amount', 'notes')
        }),
        ('Work Logs', {
            'fields': ('work_logs',)
        }),
    )
