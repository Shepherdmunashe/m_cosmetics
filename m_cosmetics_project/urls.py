from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', include('delivery.urls')),
    path('', include('orders.urls')),
    path('', include('payments.urls')),
    path('', include('inventory.urls')),
    path('', include('whatsapp_integration.urls')),
    path('', include('ai_assistant.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)