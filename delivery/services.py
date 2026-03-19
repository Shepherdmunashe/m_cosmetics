from .models import DeliveryZone


class DeliveryCalculator:

    @staticmethod
    def get_active_zones():
        return DeliveryZone.objects.filter(is_active=True).order_by('area_name')

    @staticmethod
    def get_zone(zone_id):
        try:
            return DeliveryZone.objects.get(pk=zone_id, is_active=True)
        except DeliveryZone.DoesNotExist:
            return None

    @staticmethod
    def calculate(zone_id):
        zone = DeliveryCalculator.get_zone(zone_id)
        if zone is None:
            return None
        return {
            'zone': zone,
            'fee': zone.price,
            'estimated_time': zone.estimated_delivery_time,
        }
