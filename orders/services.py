from decimal import Decimal
from .models import Order, OrderItem
from delivery.services import DeliveryCalculator
from inventory.services import InventoryService


class OrderService:

    @staticmethod
    def create_order(customer_data: dict, cart_items: list, delivery_zone_id, payment_method: str) -> Order:
        """
        Create an Order from cart data.
        customer_data: {'name', 'phone', 'email', 'address', 'notes'}
        cart_items:    [{'id', 'name', 'price', 'quantity'}, ...]
        """
        delivery_info = DeliveryCalculator.calculate(delivery_zone_id) if delivery_zone_id else None
        delivery_zone = delivery_info['zone'] if delivery_info else None
        delivery_fee = delivery_info['fee'] if delivery_info else Decimal('0')

        cart_total = sum(
            Decimal(str(item['price'])) * int(item['quantity'])
            for item in cart_items
        )
        total = cart_total + delivery_fee

        order = Order.objects.create(
            customer_name=customer_data.get('name', ''),
            phone=customer_data.get('phone', ''),
            email=customer_data.get('email', ''),
            delivery_zone=delivery_zone,
            delivery_address=customer_data.get('address', ''),
            cart_total=cart_total,
            delivery_fee=delivery_fee,
            total_price=total,
            payment_method=payment_method,
            notes=customer_data.get('notes', ''),
        )

        for item in cart_items:
            from store.models import Product
            product = None
            try:
                product = Product.objects.get(pk=int(item['id']))
            except (Product.DoesNotExist, (KeyError, ValueError)):
                pass

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item['name'],
                quantity=int(item['quantity']),
                price=Decimal(str(item['price'])),
            )

            if product:
                InventoryService.reduce_stock(product, int(item['quantity']), order.order_number)

        return order

    @staticmethod
    def update_payment_status(order: Order, status: str):
        order.payment_status = status
        if status == 'paid':
            order.order_status = 'confirmed'
        elif status == 'failed':
            order.order_status = 'cancelled'
        order.save(update_fields=['payment_status', 'order_status', 'updated_at'])

    @staticmethod
    def update_order_status(order: Order, status: str):
        order.order_status = status
        order.save(update_fields=['order_status', 'updated_at'])
