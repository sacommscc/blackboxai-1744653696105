from django.contrib import admin
from .models import (
    ReportTemplate, SavedReport, TaxConfiguration,
    AnalyticsConfiguration, ScheduledReport
)

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'created_by', 'is_active', 'created_at')
    list_filter = ('report_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'template', 'generated_by',
        'date_range_start', 'date_range_end', 'created_at'
    )
    list_filter = ('template', 'export_format', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('generated_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set generated_by during the first save
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(TaxConfiguration)
class TaxConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_rate', 'is_active', 'effective_from', 'effective_to')
    list_filter = ('is_active', 'effective_from')
    search_fields = ('name', 'description')
    date_hierarchy = 'effective_from'

@admin.register(AnalyticsConfiguration)
class AnalyticsConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'chart_type', 'refresh_interval',
        'is_active', 'created_by', 'created_at'
    )
    list_filter = ('chart_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'template', 'frequency',
        'is_active', 'next_generation', 'created_by'
    )
    list_filter = ('frequency', 'is_active', 'template')
    search_fields = ('name', 'description')
    date_hierarchy = 'next_generation'
    filter_horizontal = ('recipients',)
    readonly_fields = (
        'created_by', 'created_at', 'updated_at',
        'last_generated'
    )
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'template')
        }),
        ('Schedule', {
            'fields': (
                'frequency', 'is_active', 'next_generation',
                'last_generated'
            )
        }),
        ('Report Configuration', {
            'fields': ('parameters', 'export_format')
        }),
        ('Recipients', {
            'fields': ('recipients',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
