from django.contrib import admin
from .models import MaterialType, Vendor, VendorProduct, Purchase, Payment

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'phone', 'email')
    filter_horizontal = ('material_types',)

@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'material_type', 'price_per_unit', 'unit_type')
    list_filter = ('material_type', 'unit_type', 'vendor')
    search_fields = ('name', 'vendor__name')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'product', 'quantity', 'total_amount', 'purchase_date', 'payment_status')
    list_filter = ('payment_status', 'payment_method', 'purchase_date')
    search_fields = ('vendor__name', 'product__name')
    date_hierarchy = 'purchase_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'amount', 'payment_date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('purchase__vendor__name', 'transaction_id')
    date_hierarchy = 'payment_date'
