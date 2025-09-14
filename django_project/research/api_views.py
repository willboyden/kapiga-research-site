"""
API views for Dr. Saidi Kapiga's research data
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import (
    ResearchStudy, Publication, Researcher, Institution, 
    Dataset, ResearchCategory
)
from .serializers import (
    ResearchStudySerializer, PublicationSerializer, 
    ResearcherSerializer, InstitutionSerializer, DatasetSerializer
)


class ResearchStudyViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for research studies"""
    queryset = ResearchStudy.objects.all()
    serializer_class = ResearchStudySerializer
    
    def get_queryset(self):
        queryset = ResearchStudy.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by study type
        study_type = self.request.query_params.get('type', None)
        if study_type:
            queryset = queryset.filter(study_type=study_type)
        
        # Filter by publication status
        published = self.request.query_params.get('published', None)
        if published is not None:
            queryset = queryset.filter(is_published=published.lower() == 'true')
        
        return queryset.order_by('-publication_date')


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for publications"""
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    
    def get_queryset(self):
        queryset = Publication.objects.all()
        
        # Filter by year
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(publication_date__year=year)
        
        # Filter by journal
        journal = self.request.query_params.get('journal', None)
        if journal:
            queryset = queryset.filter(journal__icontains=journal)
        
        return queryset.order_by('-publication_date')


class ResearcherViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for researchers"""
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for institutions"""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for public datasets"""
    queryset = Dataset.objects.filter(is_public=True)
    serializer_class = DatasetSerializer


@api_view(['GET'])
def analytics_summary(request):
    """Provide analytics summary data"""
    try:
        data = {
            'total_studies': ResearchStudy.objects.count(),
            'total_publications': Publication.objects.count(),
            'total_researchers': Researcher.objects.count(),
            'total_institutions': Institution.objects.count(),
            'published_studies': ResearchStudy.objects.filter(is_published=True).count(),
            'ongoing_studies': ResearchStudy.objects.filter(
                is_published=False, 
                end_date__isnull=True
            ).count(),
            
            # Studies by type
            'studies_by_type': list(
                ResearchStudy.objects.values('study_type')
                .annotate(count=Count('id'))
                .order_by('-count')
            ),
            
            # Publications by year (last 10 years)
            'publications_by_year': list(
                Publication.objects.extra(
                    select={'year': "strftime('%%Y', publication_date)"}
                ).values('year')
                .annotate(count=Count('id'))
                .filter(publication_date__year__gte=2014)
                .order_by('year')
            ),
            
            # Geographic distribution
            'studies_by_location': list(
                ResearchStudy.objects.values('location')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            
            # Research categories
            'studies_by_category': list(
                ResearchCategory.objects.annotate(
                    study_count=Count('researchstudy')
                ).values('name', 'study_count')
                .order_by('-study_count')
            ),
            
            # Citation metrics
            'total_citations': sum(
                pub.citation_count for pub in Publication.objects.all()
            ),
            'avg_citations_per_paper': Publication.objects.aggregate(
                avg_citations=models.Avg('citation_count')
            )['avg_citations'] or 0,
        }
        
        return Response(data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def studies_by_location(request):
    """Get studies grouped by geographic location"""
    try:
        locations = ResearchStudy.objects.values('location').annotate(
            study_count=Count('id'),
            published_count=Count('id', filter=Q(is_published=True))
        ).order_by('-study_count')
        
        return Response(list(locations))
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def collaboration_network(request):
    """Get institution collaboration network data"""
    try:
        # Get all institutions and their collaborations
        institutions = Institution.objects.all()
        collaborations = {}
        
        # Calculate collaboration strength between institutions
        for study in ResearchStudy.objects.prefetch_related('institutions'):
            study_institutions = list(study.institutions.all())
            for i, inst1 in enumerate(study_institutions):
                for inst2 in study_institutions[i+1:]:
                    key = tuple(sorted([inst1.id, inst2.id]))
                    collaborations[key] = collaborations.get(key, 0) + 1
        
        # Prepare network data
        nodes = []
        for institution in institutions:
            study_count = institution.researchstudy_set.count()
            nodes.append({
                'id': institution.id,
                'label': institution.name,
                'country': institution.country,
                'type': institution.type,
                'study_count': study_count,
                'size': min(50, max(10, study_count * 5))  # Node size based on activity
            })
        
        edges = []
        for (inst1_id, inst2_id), weight in collaborations.items():
            if weight >= 1:  # Only include collaborations with at least 1 shared study
                edges.append({
                    'from': inst1_id,
                    'to': inst2_id,
                    'weight': weight,
                    'width': min(10, weight * 2)  # Edge width based on collaboration strength
                })
        
        return Response({
            'nodes': nodes,
            'edges': edges,
            'collaboration_stats': {
                'total_collaborations': len(collaborations),
                'strongest_collaboration': max(collaborations.values()) if collaborations else 0,
                'average_collaboration_strength': sum(collaborations.values()) / len(collaborations) if collaborations else 0
            }
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
