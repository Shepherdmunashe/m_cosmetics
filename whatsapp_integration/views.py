import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import WhatsAppService
from delivery.services import DeliveryCalculator


@require_POST
def whatsapp_order_url(request):
    """AJAX endpoint: receives cart JSON + delivery zone, returns WhatsApp URL."""
    try:
        data = json.loads(request.body)
        cart_items = data.get('cart', [])
        zone_id = data.get('delivery_zone_id')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    delivery_zone = None
    if zone_id:
        delivery_zone = DeliveryCalculator.get_zone(zone_id)

    service = WhatsAppService()
    url = service.generate_cart_order_url(cart_items, delivery_zone)
    return JsonResponse({'url': url})
