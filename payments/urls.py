from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:order_id>/pay/', views.initiate_paynow, name='initiate_paynow'),
    path('payment/return/', views.payment_return, name='payment_return'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/<int:order_id>/status/', views.payment_status, name='payment_status'),
]
