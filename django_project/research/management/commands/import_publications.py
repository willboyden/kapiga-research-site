import csv
from django.core.management.base import BaseCommand
from research.models import Publication, ResearchStudy, ResearchCategory

class Command(BaseCommand):
    help = 'Import publications from kapiga_publications.csv'

    def handle(self, *args, **options):
        with open('data/kapiga_publications.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Get or create related study and category
                sample_size = row.get('sample_size')
                try:
                    sample_size = int(float(sample_size)) if sample_size else None
                except ValueError:
                    sample_size = None
                category, _ = ResearchCategory.objects.get_or_create(
                    name=row.get('research_category', 'Uncategorized')
                )
                study, _ = ResearchStudy.objects.get_or_create(
                    title=row.get('title', '') + ' Study',
                    defaults={
                        'study_type': row.get('study_type', ''),
                        'location': row.get('location', ''),
                        'sample_size': sample_size,
                        'description': f"Auto-generated for publication: {row.get('title', '')}",
                        'category': category
                    }
                )
                category, _ = ResearchCategory.objects.get_or_create(
                    name=row.get('research_category', 'Uncategorized')
                )
                Publication.objects.create(
                    title=row['title'],
                    journal=row['journal'],
                    publication_date=f"{row['year']}-01-01",
                    citation_count=int(row['citation_count'] or 0),
                    study=study,
                    authors='',
                )
        self.stdout.write(self.style.SUCCESS('Imported publications from kapiga_publications.csv'))
