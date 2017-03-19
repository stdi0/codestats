from django.core.management.base import BaseCommand
from index.views import new_day


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_day()
