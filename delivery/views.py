from django.http import JsonResponse
from .services import DeliveryCalculator


def delivery_zones_api(request):
    zones = DeliveryCalculator.get_active_zones()
    data = [
        {
            'id': z.id,
            'area_name': z.area_name,
            'price': str(z.price),
            'estimated_delivery_time': z.estimated_delivery_time,
        }
        for z in zones
    ]
    return JsonResponse({'zones': data})
