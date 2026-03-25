import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import WhatsAppService
from delivery.services import DeliveryCalculator


@csrf_exempt
def webhook(request):
    """Meta webhook: GET = verification challenge, POST = incoming messages."""
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == settings.WA_VERIFY_TOKEN:
            return HttpResponse(challenge, content_type='text/plain')
        return HttpResponseForbidden('Verification failed')

    if request.method == 'POST':
        # Incoming message events — handle as needed
        return HttpResponse('OK', status=200)

    return HttpResponseForbidden()


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
