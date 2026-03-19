from django.db import models


class StockHistory(models.Model):
    REASON_CHOICES = [
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('adjustment', 'Manual Adjustment'),
        ('return', 'Return'),
    ]

    product = models.ForeignKey(
        'store.Product', related_name='stock_history', on_delete=models.CASCADE
    )
    quantity_change = models.IntegerField(help_text='Negative = stock out, Positive = stock in')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default='sale')
    reference = models.CharField(max_length=100, blank=True, help_text='Order number or note')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.quantity_change > 0 else ''
        return f"{self.product.name}: {sign}{self.quantity_change} ({self.reason})"
