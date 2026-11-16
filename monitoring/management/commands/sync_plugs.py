from django.core.management.base import BaseCommand
from monitoring.services import sync_all_devices

class Command(BaseCommand):
    def handle(self, *args, **options):
        saved_readings = sync_all_devices()
        count = len(saved_readings)

        if count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully synced {count} device readings.")
            )

        else: 
            self.stdout.write(
                self.style.WARNING(f"No readings, check if devices are configured and online.")

            )
