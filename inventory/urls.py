from django.urls import path
from . import views

urlpatterns = [
    path('admin/inventory/', views.inventory_dashboard, name='inventory_dashboard'),
    path('admin/inventory/<int:product_id>/restock/', views.restock_product, name='restock_product'),
]
