import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy

class Command(BaseCommand):
    help = 'Import trial comparison data from trial_comparison.csv'

    def handle(self, *args, **options):
        with open('data/trial_comparison.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sample_size = row.get('Sample_Size')
                try:
                    sample_size = int(float(sample_size)) if sample_size else None
                except ValueError:
                    sample_size = None
                from research.models import ResearchCategory
                category, _ = ResearchCategory.objects.get_or_create(name='Uncategorized')
                ResearchStudy.objects.get_or_create(
                    title=row['Trial'],
                    defaults={
                        'description': row['Key_Learning'],
                        'sample_size': sample_size,
                        'study_type': '',
                        'location': '',
                        'category': category
                    }
                )
        self.stdout.write(self.style.SUCCESS('Imported trial comparison data from trial_comparison.csv'))
