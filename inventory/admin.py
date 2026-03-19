from django.contrib import admin
from .models import StockHistory


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_change', 'reason', 'reference', 'created_at')
    list_filter = ('reason', 'created_at')
    readonly_fields = ('product', 'quantity_change', 'reason', 'reference', 'created_at')
    search_fields = ('product__name', 'reference')
