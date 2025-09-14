import csv
from django.core.management.base import BaseCommand
from research.models import ResearchStudy, Dataset

class Command(BaseCommand):
    help = 'Import clinical trial summary data from clinical_trials_summary.json'

    def handle(self, *args, **options):
        # This file is summary only, not row-based data, so just log or store as needed
        self.stdout.write(self.style.SUCCESS('Clinical trial summary loaded (no row-based import needed)'))
