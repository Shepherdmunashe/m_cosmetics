from django.core.management.base import BaseCommand
from delivery.models import DeliveryZone


ZONES = [
    {'area_name': 'CBD / City Centre',  'price': '3.00', 'estimated_delivery_time': '30-60 min'},
    {'area_name': 'Avondale',           'price': '4.00', 'estimated_delivery_time': '45-90 min'},
    {'area_name': 'Borrowdale',         'price': '5.00', 'estimated_delivery_time': '1-2 hours'},
    {'area_name': 'Greendale',          'price': '4.50', 'estimated_delivery_time': '1-2 hours'},
    {'area_name': 'Mabelreign',         'price': '4.00', 'estimated_delivery_time': '45-90 min'},
    {'area_name': 'Hatfield',           'price': '4.50', 'estimated_delivery_time': '1-2 hours'},
    {'area_name': 'Chitungwiza',        'price': '6.00', 'estimated_delivery_time': '2-3 hours'},
    {'area_name': 'Ruwa',               'price': '6.00', 'estimated_delivery_time': '2-3 hours'},
    {'area_name': 'Epworth',            'price': '5.00', 'estimated_delivery_time': '1.5-2.5 hours'},
    {'area_name': 'Norton',             'price': '8.00', 'estimated_delivery_time': '2-4 hours'},
]


class Command(BaseCommand):
    help = 'Seed the database with default delivery zones for Harare'

    def handle(self, *args, **options):
        created = 0
        for zone_data in ZONES:
            obj, was_created = DeliveryZone.objects.get_or_create(
                area_name=zone_data['area_name'],
                defaults={
                    'price': zone_data['price'],
                    'estimated_delivery_time': zone_data['estimated_delivery_time'],
                    'is_active': True,
                },
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {obj}'))
            else:
                self.stdout.write(f'  Already exists: {obj}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. {created} new zones created.'))
