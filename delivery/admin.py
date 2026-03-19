from django.contrib import admin
from .models import DeliveryZone


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'price', 'estimated_delivery_time', 'is_active')
    list_editable = ('price', 'is_active')
    search_fields = ('area_name',)
