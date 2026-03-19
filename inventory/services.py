from django.db.models import F
from .models import StockHistory


class InventoryService:

    @staticmethod
    def reduce_stock(product, quantity: int, reference: str = '') -> None:
        """Reduce stock after a sale. Auto-marks out of stock when qty reaches 0."""
        product.stock_quantity = max(0, product.stock_quantity - quantity)
        if product.stock_quantity == 0:
            product.in_stock = False
        product.save(update_fields=['stock_quantity', 'in_stock'])

        StockHistory.objects.create(
            product=product,
            quantity_change=-quantity,
            reason='sale',
            reference=reference,
        )

    @staticmethod
    def restock(product, quantity: int, reference: str = '') -> None:
        """Increase stock. Marks product back in stock."""
        product.stock_quantity += quantity
        product.in_stock = True
        product.save(update_fields=['stock_quantity', 'in_stock'])

        StockHistory.objects.create(
            product=product,
            quantity_change=quantity,
            reason='restock',
            reference=reference,
        )

    @staticmethod
    def adjust_stock(product, new_quantity: int, reference: str = '') -> None:
        """Set absolute stock quantity (manual adjustment)."""
        old_qty = product.stock_quantity
        change = new_quantity - old_qty
        product.stock_quantity = max(0, new_quantity)
        product.in_stock = product.stock_quantity > 0
        product.save(update_fields=['stock_quantity', 'in_stock'])

        if change != 0:
            StockHistory.objects.create(
                product=product,
                quantity_change=change,
                reason='adjustment',
                reference=reference or 'Manual adjustment',
            )

    @staticmethod
    def get_low_stock_products():
        from store.models import Product
        return Product.objects.filter(
            stock_quantity__gt=0,
            stock_quantity__lte=F('low_stock_threshold'),
        )

    @staticmethod
    def get_out_of_stock_products():
        from store.models import Product
        return Product.objects.filter(stock_quantity=0)

    @staticmethod
    def get_dashboard_stats():
        from store.models import Product
        from orders.models import Order
        all_products = Product.objects.all()
        return {
            'total_products': all_products.count(),
            'in_stock_count': all_products.filter(in_stock=True).count(),
            'out_of_stock_count': all_products.filter(in_stock=False).count(),
            'low_stock_products': InventoryService.get_low_stock_products(),
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(order_status='pending').count(),
            'recent_orders': Order.objects.select_related('delivery_zone').order_by('-created_at')[:10],
        }
