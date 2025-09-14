"""
API URL configuration for research app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'studies', api_views.ResearchStudyViewSet)
router.register(r'publications', api_views.PublicationViewSet)
router.register(r'researchers', api_views.ResearcherViewSet)
router.register(r'institutions', api_views.InstitutionViewSet)
router.register(r'datasets', api_views.DatasetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/summary/', api_views.analytics_summary, name='analytics_summary'),
    path('studies/by-location/', api_views.studies_by_location, name='studies_by_location'),
    path('collaboration-network/', api_views.collaboration_network, name='collaboration_network'),
]
