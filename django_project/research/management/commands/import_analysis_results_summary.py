import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy, Dataset

class Command(BaseCommand):
    help = 'Import analysis results from analysis_results.json'

    def handle(self, *args, **options):
        # This file is summary only, not row-based data, so just log or store as needed
        self.stdout.write(self.style.SUCCESS('Analysis results loaded (no row-based import needed)'))
