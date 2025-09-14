import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy, Dataset

class Command(BaseCommand):
    help = 'Import FEM-PrEP results from fem_prep_results.csv'

    def handle(self, *args, **options):
        with open('data/fem_prep_results.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                study, _ = ResearchStudy.objects.get_or_create(
                    title='FEM-PrEP',
                    defaults={'description': 'FEM-PrEP trial'}
                )
                Dataset.objects.get_or_create(
                    name=f"FEM-PrEP Results - {row['site']}",
                    study=study,
                    defaults={
                        'description': f"Results for {row['site']}",
                        'file_format': 'csv',
                        'file_path': 'data/fem_prep_results.csv'
                    }
                )
        self.stdout.write(self.style.SUCCESS('Imported FEM-PrEP results from fem_prep_results.csv'))
