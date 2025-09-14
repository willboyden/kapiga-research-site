"""
Serializers for Dr. Saidi Kapiga's research API
"""
from rest_framework import serializers
from .models import (
    ResearchStudy, Publication, Researcher, Institution, 
    Dataset, ResearchCategory, StudyParticipation
)


class ResearchCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchCategory
        fields = ['id', 'name', 'description']


class InstitutionSerializer(serializers.ModelSerializer):
    study_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Institution
        fields = ['id', 'name', 'country', 'type', 'website', 'study_count']
    
    def get_study_count(self, obj):
        return obj.researchstudy_set.count()


class ResearcherSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    
    class Meta:
        model = Researcher
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 
            'email', 'institution_name', 'title', 'bio', 
            'is_principal_investigator'
        ]


class StudyParticipationSerializer(serializers.ModelSerializer):
    researcher = ResearcherSerializer(read_only=True)
    
    class Meta:
        model = StudyParticipation
        fields = ['researcher', 'role']


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'authors', 'journal', 'volume', 
            'issue', 'pages', 'publication_date', 'doi', 
            'pmid', 'citation_count', 'impact_factor'
        ]


class ResearchStudySerializer(serializers.ModelSerializer):
    category = ResearchCategorySerializer(read_only=True)
    institutions = InstitutionSerializer(many=True, read_only=True)
    researchers = StudyParticipationSerializer(
        source='studyparticipation_set', 
        many=True, 
        read_only=True
    )
    publications = PublicationSerializer(
        source='publication_set', 
        many=True, 
        read_only=True
    )
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = ResearchStudy
        fields = [
            'id', 'title', 'description', 'abstract', 'category',
            'institutions', 'researchers', 'publications',
            'study_type', 'start_date', 'end_date', 'duration_days',
            'sample_size', 'location', 'is_published', 
            'publication_date', 'journal', 'doi', 'pmid'
        ]
    
    def get_duration_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None


class DatasetSerializer(serializers.ModelSerializer):
    study_title = serializers.CharField(source='study.title', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'description', 'study_title', 
            'file_format', 'size_mb', 'created_at', 'is_public'
        ]


class ResearchStudyListSerializer(serializers.ModelSerializer):
    """Simplified serializer for study lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    institution_count = serializers.SerializerMethodField()
    publication_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ResearchStudy
        fields = [
            'id', 'title', 'category_name', 'study_type', 
            'start_date', 'end_date', 'sample_size', 'location',
            'is_published', 'institution_count', 'publication_count'
        ]
    
    def get_institution_count(self, obj):
        return obj.institutions.count()
    
    def get_publication_count(self, obj):
        return obj.publication_set.count()


class PublicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for publication lists"""
    study_title = serializers.CharField(source='study.title', read_only=True)
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'journal', 'publication_date', 
            'citation_count', 'study_title'
        ]
