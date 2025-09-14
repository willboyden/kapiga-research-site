from django.apps import AppConfig


class ResearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'research'
    verbose_name = 'HIV Research in Africa'
    
    def ready(self):
        # Import signals here if needed
        pass
