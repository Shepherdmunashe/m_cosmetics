from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store.views import admin_only
from store.models import Product
from .services import AIService


@admin_only
def ai_panel(request):
    products = Product.objects.order_by('name')
    return render(request, 'ai_assistant/panel.html', {'products': products})


@admin_only
@require_POST
def ai_generate(request):
    action = request.POST.get('action')
    product_name = request.POST.get('product_name', '').strip()
    category = request.POST.get('category', '').strip()
    price = request.POST.get('price', '').strip()
    question = request.POST.get('question', '').strip()

    if not product_name and action != 'answer_question':
        return JsonResponse({'error': 'Product name is required.'}, status=400)

    service = AIService()

    action_map = {
        'description': lambda: service.generate_product_description(product_name, category, price),
        'caption': lambda: service.generate_instagram_caption(product_name, category),
        'marketing': lambda: service.generate_marketing_copy(product_name),
        'hashtags': lambda: service.suggest_hashtags(product_name, category),
        'answer_question': lambda: service.answer_store_question(question),
    }

    handler = action_map.get(action)
    if not handler:
        return JsonResponse({'error': 'Invalid action.'}, status=400)

    result = handler()
    return JsonResponse({'result': result})
