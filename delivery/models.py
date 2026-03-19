from django.db import models


class DeliveryZone(models.Model):
    area_name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=50, help_text='e.g. 1-2 hours')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['area_name']

    def __str__(self):
        return f"{self.area_name} (${self.price})"
