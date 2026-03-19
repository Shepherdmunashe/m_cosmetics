from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'subtotal')

    def subtotal(self, obj):
        return f"${obj.subtotal}"
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'phone', 'delivery_zone', 'total_price', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_status', 'order_status', 'payment_method', 'created_at')
    list_editable = ('payment_status', 'order_status')
    search_fields = ('customer_name', 'phone', 'email')
    readonly_fields = ('cart_total', 'delivery_fee', 'total_price', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
