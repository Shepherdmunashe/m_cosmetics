from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'paynow_reference', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('order', 'paynow_reference', 'poll_url', 'amount', 'raw_response', 'created_at', 'updated_at')
