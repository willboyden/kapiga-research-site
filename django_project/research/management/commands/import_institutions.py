import csv
from django.core.management.base import BaseCommand
from research.models import Institution

class Command(BaseCommand):
    help = 'Import institutions from collaboration_network.csv'

    def handle(self, *args, **options):
        with open('data/collaboration_network.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Institution.objects.get_or_create(
                    name=row['institution'],
                    defaults={
                        'country': row['country']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Imported institutions from collaboration_network.csv'))
