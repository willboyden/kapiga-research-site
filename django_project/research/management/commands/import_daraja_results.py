import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy, Dataset

class Command(BaseCommand):
    help = 'Import Daraja results from daraja_results.csv'

    def handle(self, *args, **options):
        with open('data/daraja_results.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            study, _ = ResearchStudy.objects.get_or_create(
                title='Daraja Trial',
                defaults={'description': 'Daraja social worker intervention trial'}
            )
            Dataset.objects.get_or_create(
                name='Daraja Results',
                study=study,
                defaults={
                    'description': 'Daraja trial results',
                    'file_format': 'csv',
                    'file_path': 'data/daraja_results.csv'
                }
            )
        self.stdout.write(self.style.SUCCESS('Imported Daraja results from daraja_results.csv'))
