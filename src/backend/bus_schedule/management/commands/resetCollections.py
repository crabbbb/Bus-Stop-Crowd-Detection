from django.core.management.base import BaseCommand
from backend.utils.setup import resetCollections

# python manage.py resetCollections
class Command(BaseCommand):
    help = "Reset MongoDB collections and enter all the preset data"

    def handle(self, *args, **kwargs):
        resetCollections()
        self.stdout.write(self.style.SUCCESS("Collections reset success"))