from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib import messages

from orders.models import Order
from orders.services import OrderService
from .models import Payment
from .services import PaynowService


def initiate_paynow(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if hasattr(order, 'payment') and order.payment.status == 'paid':
        return redirect('order_confirmation', order_id=order.pk)

    service = PaynowService()
    result = service.initiate_payment(order)

    if result['success']:
        return redirect(result['redirect_url'])
    else:
        messages.error(request, f"Payment initiation failed: {result.get('error', 'Unknown error')}")
        return render(request, 'payments/payment_error.html', {'order': order, 'error': result.get('error')})


def payment_return(request):
    """Paynow redirects the customer here after payment attempt."""
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, pk=order_id)
        payment = Payment.objects.filter(order=order).first()

        if payment and payment.poll_url:
            service = PaynowService()
            status = service.check_status(payment.poll_url)
            if status.get('paid'):
                OrderService.update_payment_status(order, 'paid')
                payment.status = 'paid'
                payment.save(update_fields=['status', 'updated_at'])

        return redirect('order_confirmation', order_id=order.pk)
    return redirect('product_list')


@csrf_exempt
@require_POST
def payment_callback(request):
    """IPN webhook — Paynow posts payment status here."""
    service = PaynowService()
    service.handle_ipn(request.POST.dict())
    return HttpResponse('OK', status=200)


def payment_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    payment = Payment.objects.filter(order=order).first()

    if payment and payment.poll_url:
        service = PaynowService()
        status = service.check_status(payment.poll_url)
        if status.get('paid') and payment.status != 'paid':
            payment.status = 'paid'
            payment.save(update_fields=['status', 'updated_at'])
            OrderService.update_payment_status(order, 'paid')

    return render(request, 'payments/payment_status.html', {'order': order, 'payment': payment})
