import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy

class Command(BaseCommand):
    help = 'Import clinical trials from clinical_trials.csv'

    def handle(self, *args, **options):
        with open('data/clinical_trials.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sample_size = row.get('sample_size')
                try:
                    sample_size = int(float(sample_size)) if sample_size else None
                except ValueError:
                    sample_size = None
                # Assign a default category if needed
                from research.models import ResearchCategory
                category, _ = ResearchCategory.objects.get_or_create(name='Uncategorized')
                ResearchStudy.objects.get_or_create(
                    title=row['trial_name'],
                    defaults={
                        'description': row['full_name'],
                        'study_type': row['design'],
                        'sample_size': sample_size,
                        'location': row['locations'],
                        'category': category
                    }
                )
        self.stdout.write(self.style.SUCCESS('Imported clinical trials from clinical_trials.csv'))
