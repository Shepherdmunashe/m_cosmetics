from django.urls import path
from . import views

urlpatterns = [
    path('api/whatsapp-order/', views.whatsapp_order_url, name='whatsapp_order_url'),
]
