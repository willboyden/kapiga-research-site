"""
Django models for Dr. Saidi Kapiga's HIV Research in Africa
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ResearchCategory(models.Model):
    """Categories of research studies"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Research Categories"
    
    def __str__(self):
        return self.name


class Institution(models.Model):
    """Partner institutions in research"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('university', 'University'),
        ('research_institute', 'Research Institute'),
        ('hospital', 'Hospital'),
        ('ngo', 'NGO'),
        ('government', 'Government Agency'),
    ])
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.country})"


class ResearchStudy(models.Model):
    """Individual research studies and trials"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    abstract = models.TextField(blank=True)
    category = models.ForeignKey(ResearchCategory, on_delete=models.CASCADE)
    institutions = models.ManyToManyField(Institution)
    
    # Study details
    study_type = models.CharField(max_length=50, choices=[
        ('rct', 'Randomized Controlled Trial'),
        ('cohort', 'Cohort Study'),
        ('cross_sectional', 'Cross-sectional Study'),
        ('case_control', 'Case-control Study'),
        ('systematic_review', 'Systematic Review'),
        ('meta_analysis', 'Meta-analysis'),
    ])
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sample_size = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=200)
    
    # Publication details
    is_published = models.BooleanField(default=False)
    publication_date = models.DateField(null=True, blank=True)
    journal = models.CharField(max_length=200, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    pmid = models.CharField(max_length=20, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publication_date', '-created_at']
    
    def __str__(self):
        return self.title


class Researcher(models.Model):
    """Researchers and collaborators"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    is_principal_investigator = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudyParticipation(models.Model):
    """Link researchers to studies with their roles"""
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    study = models.ForeignKey(ResearchStudy, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[
        ('pi', 'Principal Investigator'),
        ('co_pi', 'Co-Principal Investigator'),
        ('investigator', 'Investigator'),
        ('co_investigator', 'Co-Investigator'),
        ('statistician', 'Statistician'),
        ('data_manager', 'Data Manager'),
    ])
    
    class Meta:
        unique_together = ['researcher', 'study']
    
    def __str__(self):
        return f"{self.researcher.full_name} - {self.study.title} ({self.role})"


class Publication(models.Model):
    """Research publications and papers"""
    title = models.CharField(max_length=400)
    authors = models.TextField(help_text="Comma-separated list of authors")
    journal = models.CharField(max_length=200)
    volume = models.CharField(max_length=20, blank=True)
    issue = models.CharField(max_length=20, blank=True)
    pages = models.CharField(max_length=20, blank=True)
    publication_date = models.DateField()
    doi = models.CharField(max_length=100, blank=True)
    pmid = models.CharField(max_length=20, blank=True)
    abstract = models.TextField(blank=True)
    study = models.ForeignKey(ResearchStudy, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Citation metrics
    citation_count = models.IntegerField(default=0)
    impact_factor = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-publication_date']
    
    def __str__(self):
        return self.title


class Dataset(models.Model):
    """Research datasets"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    study = models.ForeignKey(ResearchStudy, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=500, blank=True)
    file_format = models.CharField(max_length=20, choices=[
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('spss', 'SPSS'),
        ('stata', 'Stata'),
        ('r', 'R Data'),
        ('json', 'JSON'),
    ])
    size_mb = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.study.title})"


class AnalyticsResult(models.Model):
    """Results from Python analytics"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    results = models.JSONField(default=dict)
    notebook_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.analysis_type} - {self.dataset.name}"


class ResearchTopic(models.Model):
    """Research topics and themes"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    studies = models.ManyToManyField(ResearchStudy, blank=True)
    
    def __str__(self):
        return self.name


class GeographicLocation(models.Model):
    """Geographic locations of studies"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    studies = models.ManyToManyField(ResearchStudy, blank=True)
    
    def __str__(self):
        return f"{self.name}, {self.country}"
