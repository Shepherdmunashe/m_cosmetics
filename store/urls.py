from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # Admin Panel URLs
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.manage_products, name='manage_products'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('admin/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('admin/users/', views.manage_users, name='manage_users'),
]
