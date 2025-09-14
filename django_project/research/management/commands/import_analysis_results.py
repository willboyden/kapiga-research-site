import json
from django.core.management.base import BaseCommand
from research.models import Publication, ResearchCategory

class Command(BaseCommand):
    help = 'Import analysis results from analysis_results.json'

    def handle(self, *args, **options):
        with open('data/analysis_results.json', encoding='utf-8') as f:
            data = json.load(f)
            for cat in data.get('category_analysis', []):
                category, _ = ResearchCategory.objects.get_or_create(
                    name=cat['research_category']
                )
                # Optionally update category metrics here
        self.stdout.write(self.style.SUCCESS('Imported analysis results from analysis_results.json'))
