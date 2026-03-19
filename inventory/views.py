from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from store.views import admin_only
from store.models import Product
from .services import InventoryService
from .models import StockHistory
from whatsapp_integration.services import WhatsAppService


@admin_only
def inventory_dashboard(request):
    stats = InventoryService.get_dashboard_stats()
    all_products = Product.objects.order_by('stock_quantity')
    wa_service = WhatsAppService()
    low_stock_alerts = [
        {
            'product': p,
            'alert_url': wa_service.get_low_stock_alert_url(p),
        }
        for p in stats['low_stock_products']
    ]
    return render(request, 'inventory/dashboard.html', {
        **stats,
        'all_products': all_products,
        'low_stock_alerts': low_stock_alerts,
    })


@admin_only
@require_POST
def restock_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get('quantity', 0))
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('inventory_dashboard')
    InventoryService.restock(product, quantity)
    messages.success(request, f'Restocked {product.name} by {quantity} units. New stock: {product.stock_quantity}')
    return redirect('inventory_dashboard')
