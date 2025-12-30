#!/usr/bin/env python
import os
import django # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm_cosmetics_project.settings')
django.setup()

from store.models import Product

# Sample products
products_data = [
    {
        'name': 'Elegant Rose Perfume',
        'description': 'A luxurious rose fragrance with notes of jasmine and sandalwood. Perfect for elegant occasions.',
        'price': 89.99,
        'in_stock': True
    },
    {
        'name': 'Sunset Beauty Lipstick',
        'description': 'Long-lasting, hydrating lipstick in a stunning coral shade. Applies smoothly for a perfect finish.',
        'price': 34.99,
        'in_stock': True
    },
    {
        'name': 'Gold Radiance Foundation',
        'description': 'Premium foundation with SPF 30. Provides full coverage with a natural, luminous finish.',
        'price': 54.99,
        'in_stock': True
    },
    {
        'name': 'Midnight Musk Cologne',
        'description': 'A sophisticated unisex fragrance with musk, cedar, and amber. Ideal for evening wear.',
        'price': 75.99,
        'in_stock': True
    },
    {
        'name': 'Crystal Eye Palette',
        'description': '12-shade eyeshadow palette with shimmering and matte finishes. Highly pigmented and blendable.',
        'price': 44.99,
        'in_stock': True
    },
    {
        'name': 'Ocean Breeze Perfume',
        'description': 'Refreshing citrus and aquatic notes. Perfect for daytime wear and summer occasions.',
        'price': 79.99,
        'in_stock': False
    },
    {
        'name': 'Velvet Blush Collection',
        'description': 'Set of 5 blush shades in warm and cool tones. Buildable coverage for any skin tone.',
        'price': 49.99,
        'in_stock': True
    },
    {
        'name': 'Diamond Mascara',
        'description': 'Ultra-volumizing mascara with a diamond-shaped brush. Defines and lengthens lashes beautifully.',
        'price': 39.99,
        'in_stock': True
    },
]

# Clear existing products
Product.objects.all().delete()

# Add products
for product_data in products_data:
    Product.objects.create(**product_data)
    print(f"Created: {product_data['name']}")

print(f"\nSuccessfully created {len(products_data)} products!")
