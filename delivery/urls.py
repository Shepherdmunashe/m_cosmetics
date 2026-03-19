from django.urls import path
from . import views

urlpatterns = [
    path('api/delivery-zones/', views.delivery_zones_api, name='delivery_zones_api'),
]
