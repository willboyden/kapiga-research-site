"""
Django admin configuration for Dr. Saidi Kapiga's research models
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    ResearchCategory, Institution, ResearchStudy, Researcher,
    StudyParticipation, Publication, Dataset, AnalyticsResult,
    ResearchTopic, GeographicLocation
)


@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'study_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def study_count(self, obj):
        return obj.researchstudy_set.count()
    study_count.short_description = 'Number of Studies'


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'type', 'study_count', 'website_link']
    list_filter = ['country', 'type']
    search_fields = ['name', 'country']
    
    def study_count(self, obj):
        return obj.researchstudy_set.count()
    study_count.short_description = 'Studies'
    
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">Visit</a>', obj.website)
        return '-'
    website_link.short_description = 'Website'


class StudyParticipationInline(admin.TabularInline):
    model = StudyParticipation
    extra = 1
    autocomplete_fields = ['researcher']


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1
    fields = ['title', 'journal', 'publication_date', 'doi']


@admin.register(ResearchStudy)
class ResearchStudyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'study_type', 'location', 
        'sample_size', 'is_published', 'publication_date'
    ]
    list_filter = [
        'category', 'study_type', 'is_published', 
        'publication_date', 'start_date'
    ]
    search_fields = ['title', 'description', 'location']
    filter_horizontal = ['institutions']
    inlines = [StudyParticipationInline, PublicationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'abstract', 'category')
        }),
        ('Study Details', {
            'fields': (
                'study_type', 'start_date', 'end_date', 
                'sample_size', 'location', 'institutions'
            )
        }),
        ('Publication Information', {
            'fields': (
                'is_published', 'publication_date', 
                'journal', 'doi', 'pmid'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'institution', 'title', 
        'is_principal_investigator', 'study_count'
    ]
    list_filter = ['institution', 'is_principal_investigator']
    search_fields = ['first_name', 'last_name', 'email', 'title']
    autocomplete_fields = ['institution']
    
    def study_count(self, obj):
        return obj.studyparticipation_set.count()
    study_count.short_description = 'Studies'


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'journal', 'publication_date', 
        'citation_count', 'doi_link', 'pmid_link'
    ]
    list_filter = ['journal', 'publication_date']
    search_fields = ['title', 'authors', 'journal', 'doi', 'pmid']
    autocomplete_fields = ['study']
    
    def doi_link(self, obj):
        if obj.doi:
            return format_html(
                '<a href="https://doi.org/{}" target="_blank">{}</a>', 
                obj.doi, obj.doi
            )
        return '-'
    doi_link.short_description = 'DOI'
    
    def pmid_link(self, obj):
        if obj.pmid:
            return format_html(
                '<a href="https://pubmed.ncbi.nlm.nih.gov/{}" target="_blank">{}</a>', 
                obj.pmid, obj.pmid
            )
        return '-'
    pmid_link.short_description = 'PubMed'


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'study', 'file_format', 'size_mb', 
        'is_public', 'created_at'
    ]
    list_filter = ['file_format', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'study__title']
    autocomplete_fields = ['study']


@admin.register(AnalyticsResult)
class AnalyticsResultAdmin(admin.ModelAdmin):
    list_display = [
        'dataset', 'analysis_type', 'created_by', 'created_at'
    ]
    list_filter = ['analysis_type', 'created_at']
    search_fields = ['dataset__name', 'analysis_type']
    readonly_fields = ['created_at']


@admin.register(ResearchTopic)
class ResearchTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_count']
    search_fields = ['name', 'description']
    filter_horizontal = ['studies']
    
    def study_count(self, obj):
        return obj.studies.count()
    study_count.short_description = 'Studies'


@admin.register(GeographicLocation)
class GeographicLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'region', 'study_count']
    list_filter = ['country', 'region']
    search_fields = ['name', 'country', 'region']
    filter_horizontal = ['studies']
    
    def study_count(self, obj):
        return obj.studies.count()
    study_count.short_description = 'Studies'


# Customize admin site
admin.site.site_header = "Dr. Saidi Kapiga Research Administration"
admin.site.site_title = "Research Admin"
admin.site.index_title = "HIV Research in Africa - Administrative Interface"
