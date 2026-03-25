from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp/webhook/', views.webhook, name='whatsapp_webhook'),
    path('api/whatsapp-order/', views.whatsapp_order_url, name='whatsapp_order_url'),
]
