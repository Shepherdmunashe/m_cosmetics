from django.conf import settings
from django.urls import reverse
from orders.models import Order
from orders.services import OrderService
from .models import Payment


class PaynowService:
    """
    Wrapper around the paynow Python SDK.
    Install via: pip install paynow
    Docs: https://github.com/paynow/Paynow-Python-SDK
    """

    def __init__(self):
        self.integration_id = getattr(settings, 'PAYNOW_INTEGRATION_ID', '')
        self.integration_key = getattr(settings, 'PAYNOW_INTEGRATION_KEY', '')
        self.result_url = getattr(settings, 'PAYNOW_RESULT_URL', '')
        self.return_url = getattr(settings, 'PAYNOW_RETURN_URL', '')

    def _get_paynow(self):
        from paynow import Paynow
        return Paynow(
            self.integration_id,
            self.integration_key,
            self.result_url,
            self.return_url,
        )

    def initiate_payment(self, order: Order) -> dict:
        """
        Creates a Paynow payment and returns redirect info.
        Returns: {'success': bool, 'redirect_url': str, 'poll_url': str, 'error': str}
        """
        if not self.integration_id or not self.integration_key:
            return {'success': False, 'error': 'Paynow not configured. Set PAYNOW_INTEGRATION_ID and PAYNOW_INTEGRATION_KEY in .env'}

        try:
            paynow = self._get_paynow()
            payment_ref = order.order_number
            email = order.email or 'customer@mcosmetics.co.zw'

            payment = paynow.create_payment(payment_ref, email)

            for item in order.items.all():
                payment.add(item.product_name, float(item.price * item.quantity))

            if order.delivery_fee > 0:
                payment.add('Delivery Fee', float(order.delivery_fee))

            response = paynow.send(payment)

            if response.success:
                Payment.objects.update_or_create(
                    order=order,
                    defaults={
                        'paynow_reference': payment_ref,
                        'poll_url': response.poll_url,
                        'amount': order.total_price,
                        'status': 'pending',
                        'raw_response': str(response),
                    }
                )
                return {
                    'success': True,
                    'redirect_url': response.redirect_url,
                    'poll_url': response.poll_url,
                }
            else:
                return {'success': False, 'error': 'Paynow rejected the payment request.'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def check_status(self, poll_url: str) -> dict:
        """Poll Paynow for payment status."""
        try:
            paynow = self._get_paynow()
            status = paynow.check_transaction_status(poll_url)
            return {
                'paid': status.paid,
                'status': 'paid' if status.paid else 'pending',
            }
        except Exception as e:
            return {'paid': False, 'status': 'error', 'error': str(e)}

    def handle_ipn(self, post_data: dict) -> bool:
        """
        Handle IPN (Instant Payment Notification) from Paynow.
        Returns True if payment was confirmed.
        """
        try:
            paynow = self._get_paynow()
            status = paynow.process_status_update(post_data)

            reference = post_data.get('reference', '')
            order_num = reference  # MCO-XXXXX

            order_id_str = order_num.replace('MCO-', '').lstrip('0')
            if not order_id_str:
                return False

            from orders.models import Order
            order = Order.objects.get(pk=int(order_id_str))
            payment = Payment.objects.filter(order=order).first()

            if status.paid:
                if payment:
                    payment.status = 'paid'
                    payment.save(update_fields=['status', 'updated_at'])
                OrderService.update_payment_status(order, 'paid')
                return True
            else:
                if payment:
                    payment.status = 'failed'
                    payment.save(update_fields=['status', 'updated_at'])
                OrderService.update_payment_status(order, 'failed')
                return False

        except Exception:
            return False
