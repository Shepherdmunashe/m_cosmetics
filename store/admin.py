from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'created_at')
    list_editable = ('in_stock',)
    list_filter = ('category', 'in_stock', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'category', 'description', 'price')
        }),
        ('Stock & Media', {
            'fields': ('image', 'in_stock')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
