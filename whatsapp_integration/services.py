import urllib.parse
from django.conf import settings


class WhatsAppService:
    """
    Generates wa.me deep-link URLs for ordering and stock alerts.
    Designed to be replaceable with WhatsApp Business API later.
    """

    def __init__(self):
        raw = getattr(settings, 'CONTACT_INFO', {}).get('whatsapp', '')
        self.store_phone = raw.replace('+', '').replace(' ', '').replace('-', '')

    def _encode(self, message: str) -> str:
        return urllib.parse.quote(message)

    def generate_order_url(self, order) -> str:
        message = self._format_order_message(order)
        return f"https://wa.me/{self.store_phone}?text={self._encode(message)}"

    def _format_order_message(self, order) -> str:
        lines = [
            "Hello M Cosmetics, I would like to place an order:",
            "",
        ]
        for item in order.items.all():
            lines.append(f"• {item.product_name} x{item.quantity} — ${item.price * item.quantity:.2f}")

        lines += [
            "",
            f"Subtotal: ${order.cart_total:.2f}",
        ]
        if order.delivery_zone:
            lines.append(f"Delivery ({order.delivery_zone.area_name}): ${order.delivery_fee:.2f}")

        lines += [
            f"*Total: ${order.total_price:.2f}*",
            "",
            f"Name: {order.customer_name}",
            f"Phone: {order.phone}",
        ]
        if order.delivery_address:
            lines.append(f"Address: {order.delivery_address}")
        if order.notes:
            lines.append(f"Notes: {order.notes}")
        lines.append(f"Order Ref: {order.order_number}")
        return "\n".join(lines)

    def generate_low_stock_message(self, product) -> str:
        return (
            f"⚠ Low Stock Alert\n\n"
            f"Product: {product.name}\n"
            f"Remaining: {product.stock_quantity} units\n"
            f"Threshold: {product.low_stock_threshold} units\n\n"
            f"Please restock soon."
        )

    def get_low_stock_alert_url(self, product) -> str:
        message = self.generate_low_stock_message(product)
        return f"https://wa.me/{self.store_phone}?text={self._encode(message)}"

    def generate_cart_order_url(self, cart_items: list, delivery_zone=None) -> str:
        """Generate WhatsApp URL directly from cart (client-side use via JS endpoint)."""
        lines = ["Hello M Cosmetics, I would like to order:", ""]
        total = 0.0
        for item in cart_items:
            subtotal = float(item['price']) * int(item['quantity'])
            total += subtotal
            lines.append(f"• {item['name']} x{item['quantity']} — ${subtotal:.2f}")
        lines.append("")
        lines.append(f"Subtotal: ${total:.2f}")
        if delivery_zone:
            lines.append(f"Delivery ({delivery_zone.area_name}): ${delivery_zone.price:.2f}")
            total += float(delivery_zone.price)
        lines.append(f"*Total: ${total:.2f}*")
        return f"https://wa.me/{self.store_phone}?text={self._encode(chr(10).join(lines))}"
