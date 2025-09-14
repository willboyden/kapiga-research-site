"""
Views for Dr. Saidi Kapiga's HIV Research Website
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
import pandas as pd
import numpy as np
from .models import (
    ResearchStudy, Publication, Researcher, Institution, 
    Dataset, AnalyticsResult, ResearchCategory, ResearchTopic
)


def home(request):
    """Homepage with research overview"""
    context = {
        'total_studies': ResearchStudy.objects.count(),
        'total_publications': Publication.objects.count(),
        'total_researchers': Researcher.objects.count(),
        'recent_studies': ResearchStudy.objects.filter(is_published=True)[:6],
        'featured_publications': Publication.objects.order_by('-citation_count')[:5],
        'research_categories': ResearchCategory.objects.all(),
    }
    return render(request, 'research/home.html', context)


def about_dr_kapiga(request):
    """About Dr. Saidi Kapiga"""
    context = {
        'researcher_name': 'Dr. Saidi Kapiga',
        'institution': 'London School of Hygiene & Tropical Medicine',
        'position': 'Professor of Epidemiology and International Health',
        'location': 'Mwanza Intervention Trials Unit, Tanzania',
        'experience_years': 30,
        'key_research_areas': [
            'HIV/AIDS Prevention and Treatment',
            'Sexual and Reproductive Health',
            'Intimate Partner Violence Prevention',
            'Alcohol and Substance Use Disorders',
            'Hypertension in HIV Patients',
            'Adolescent Health in Africa',
            'Clinical Trials and Interventions'
        ],
        'major_projects': [
            'Daraja Trial - Social Worker Intervention for HIV Patients',
            'FEM-PrEP Study - Pre-exposure Prophylaxis for Women',
            'MEMA kwa Vijana - Adolescent Health Intervention',
            'Lake Victoria Health Research Consortium'
        ]
    }
    return render(request, 'research/about.html', context)


class StudyListView(ListView):
    """List all research studies"""
    model = ResearchStudy
    template_name = 'research/studies.html'
    context_object_name = 'studies'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = ResearchStudy.objects.all()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        # Filter by study type
        study_type = self.request.GET.get('type')
        if study_type:
            queryset = queryset.filter(study_type=study_type)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset.order_by('-publication_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResearchCategory.objects.all()
        context['study_types'] = ResearchStudy._meta.get_field('study_type').choices
        return context


class StudyDetailView(DetailView):
    """Detailed view of a research study"""
    model = ResearchStudy
    template_name = 'research/study_detail.html'
    context_object_name = 'study'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        study = self.get_object()
        context['researchers'] = study.studyparticipation_set.all()
        context['publications'] = study.publication_set.all()
        context['datasets'] = study.dataset_set.filter(is_public=True)
        return context


class PublicationListView(ListView):
    """List all publications"""
    model = Publication
    template_name = 'research/publications.html'
    context_object_name = 'publications'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Publication.objects.all()
        search = self.request.GET.get('search')
        year = self.request.GET.get('year')
        # Only filter if a search or year is provided
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(authors__icontains=search) |
                Q(journal__icontains=search)
            )
        if year:
            queryset = queryset.filter(publication_date__year=year)
        # If no filters, always return all publications
        return queryset.order_by('-publication_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get available years for filtering
        years = Publication.objects.dates('publication_date', 'year', order='DESC')
        context['years'] = [date.year for date in years]
        return context


def analytics_dashboard(request):
    """Analytics dashboard showing research metrics"""
    # Study statistics
    studies_by_type = ResearchStudy.objects.values('study_type').annotate(
        count=Count('id')
    )
    
    # Publications by year (Postgres compatible)
    from django.db.models.functions import ExtractYear
    publications_by_year = (
        Publication.objects.annotate(year=ExtractYear('publication_date'))
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    
    # Geographic distribution
    studies_by_location = ResearchStudy.objects.values('location').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Top researchers by publication count
    top_researchers = Researcher.objects.annotate(
        pub_count=Count('studyparticipation__study__publication')
    ).order_by('-pub_count')[:10]
    
    # Publication metrics
    pubs = Publication.objects.all()
    total_citations = sum(pub.citation_count for pub in pubs)
    avg_citations = total_citations / pubs.count() if pubs.count() else 0
    # H-index calculation
    citation_list = sorted([pub.citation_count for pub in pubs], reverse=True)
    h_index = sum(1 for i, cites in enumerate(citation_list, 1) if cites >= i)
    # Unique journals
    journals = set(pub.journal for pub in pubs if pub.journal)
    context = {
        'studies_by_type': list(studies_by_type),
        'publications_by_year': list(publications_by_year),
        'studies_by_location': list(studies_by_location),
        'top_researchers': top_researchers,
        'total_citations': total_citations,
        'avg_citations': avg_citations,
        'h_index': h_index,
        'journal_count': len(journals),
    }
    return render(request, 'research/analytics.html', context)


@login_required
def dataset_analysis(request, dataset_id):
    """Perform analysis on a dataset"""
    dataset = get_object_or_404(Dataset, id=dataset_id)
    
    if request.method == 'POST':
        analysis_type = request.POST.get('analysis_type')
        
        # Simple analytics examples
        try:
            if dataset.file_format == 'csv' and dataset.file_path:
                # Load data from CSV (legacy support)
                df = pd.read_csv(dataset.file_path)
            else:
                # Try loading from database (example: publications)
                from research.models import Publication
                pubs = Publication.objects.filter(study=dataset.study)
                if pubs.exists():
                    df = pd.DataFrame({
                        'title': [p.title for p in pubs],
                        'year': [p.publication_date.year if p.publication_date else None for p in pubs],
                        'journal': [p.journal for p in pubs],
                        'citation_count': [p.citation_count for p in pubs],
                        'authors': [p.authors for p in pubs],
                    })
                else:
                    df = pd.DataFrame()
                
                results = {}
                if analysis_type == 'descriptive':
                    results = {
                        'shape': df.shape,
                        'columns': list(df.columns),
                        'dtypes': df.dtypes.to_dict(),
                        'summary': df.describe().to_dict(),
                        'missing_values': df.isnull().sum().to_dict()
                    }
                elif analysis_type == 'correlation':
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 1:
                        results = df[numeric_cols].corr().to_dict()
                
                # Save analysis result
                AnalyticsResult.objects.create(
                    dataset=dataset,
                    analysis_type=analysis_type,
                    results=results,
                    created_by=request.user
                )
                
                return JsonResponse({'success': True, 'results': results})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {
        'dataset': dataset,
        'analysis_results': dataset.analyticsresult_set.all()[:10]
    }
    return render(request, 'research/dataset_analysis.html', context)


def research_network(request):
    """Research collaboration network"""
    # Get collaboration data
    collaborations = {}
    for study in ResearchStudy.objects.prefetch_related('institutions'):
        institutions = list(study.institutions.all())
        for i, inst1 in enumerate(institutions):
            for inst2 in institutions[i+1:]:
                key = tuple(sorted([inst1.id, inst2.id]))
                collaborations[key] = collaborations.get(key, 0) + 1
    
    # Prepare network data
    nodes = []
    edges = []
    
    for institution in Institution.objects.all():
        nodes.append({
            'id': institution.id,
            'label': institution.name,
            'country': institution.country,
            'type': institution.type
        })
    
    for (inst1_id, inst2_id), weight in collaborations.items():
        edges.append({
            'from': inst1_id,
            'to': inst2_id,
            'weight': weight
        })
    
    context = {
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges)
    }
    return render(request, 'research/network.html', context)


def api_studies(request):
    """API endpoint for studies data"""
    studies = ResearchStudy.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    if category:
        studies = studies.filter(category__name=category)
    
    data = []
    for study in studies[:100]:  # Limit for performance
        data.append({
            'id': study.id,
            'title': study.title,
            'study_type': study.study_type,
            'location': study.location,
            'start_date': study.start_date.isoformat() if study.start_date else None,
            'sample_size': study.sample_size,
            'is_published': study.is_published
        })
    
    return JsonResponse({'studies': data})


def export_data(request, format_type='csv'):
    """Export research data in various formats"""
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="kapiga_research_studies.csv"'
        
        import csv
        writer = csv.writer(response)
        writer.writerow(['Title', 'Type', 'Location', 'Start Date', 'Sample Size', 'Published'])
        
        for study in ResearchStudy.objects.all():
            writer.writerow([
                study.title,
                study.study_type,
                study.location,
                study.start_date,
                study.sample_size,
                study.is_published
            ])
        
        return response
    
    # Add other export formats as needed
    return JsonResponse({'error': 'Format not supported'})
