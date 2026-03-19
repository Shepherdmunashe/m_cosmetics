import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from delivery.services import DeliveryCalculator
from whatsapp_integration.services import WhatsAppService
from .models import Order
from .services import OrderService
from store.views import admin_only


def checkout(request):
    zones = DeliveryCalculator.get_active_zones()

    if request.method == 'POST':
        cart_json = request.POST.get('cart_data', '[]')
        try:
            cart_items = json.loads(cart_json)
        except json.JSONDecodeError:
            cart_items = []

        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('product_list')

        customer_data = {
            'name': request.POST.get('customer_name', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'address': request.POST.get('delivery_address', '').strip(),
            'notes': request.POST.get('notes', '').strip(),
        }
        if not customer_data['name'] or not customer_data['phone']:
            messages.error(request, 'Name and phone number are required.')
            return render(request, 'orders/checkout.html', {'zones': zones, 'error': True})

        delivery_zone_id = request.POST.get('delivery_zone') or None
        payment_method = request.POST.get('payment_method', 'cod')

        order = OrderService.create_order(customer_data, cart_items, delivery_zone_id, payment_method)

        if payment_method == 'paynow':
            return redirect('initiate_paynow', order_id=order.pk)
        elif payment_method == 'whatsapp':
            wa_service = WhatsAppService()
            whatsapp_url = wa_service.generate_order_url(order)
            return redirect(whatsapp_url)
        else:
            return redirect('order_confirmation', order_id=order.pk)

    return render(request, 'orders/checkout.html', {'zones': zones})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    wa_service = WhatsAppService()
    whatsapp_url = wa_service.generate_order_url(order)
    return render(request, 'orders/order_confirmation.html', {
        'order': order,
        'whatsapp_url': whatsapp_url,
    })


@admin_only
def admin_order_list(request):
    orders = Order.objects.select_related('delivery_zone').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    return render(request, 'orders/admin_order_list.html', {
        'orders': orders,
        'status_filter': status_filter,
        'order_status_choices': Order.ORDER_STATUS_CHOICES,
    })


@admin_only
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            new_status = request.POST.get('order_status')
            if new_status:
                OrderService.update_order_status(order, new_status)
                messages.success(request, f'Order status updated to {new_status}.')
        elif action == 'update_payment':
            new_payment = request.POST.get('payment_status')
            if new_payment:
                OrderService.update_payment_status(order, new_payment)
                messages.success(request, f'Payment status updated to {new_payment}.')
        return redirect('admin_order_detail', order_id=order.pk)

    wa_service = WhatsAppService()
    return render(request, 'orders/admin_order_detail.html', {
        'order': order,
        'order_status_choices': Order.ORDER_STATUS_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
        'whatsapp_url': wa_service.generate_order_url(order),
    })
