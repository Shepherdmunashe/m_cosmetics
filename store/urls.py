from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_results, name='search_results'),
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

    # Category Management URLs
    path('admin/categories/', views.manage_categories, name='manage_categories'),
    path('admin/categories/add/', views.add_category, name='add_category'),
    path('admin/categories/add-inline/', views.add_category_inline, name='add_category_inline'),
    path('admin/categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('admin/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]
