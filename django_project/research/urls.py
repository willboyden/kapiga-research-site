"""
URL configuration for research app
"""
from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_dr_kapiga, name='about'),
    path('studies/', views.StudyListView.as_view(), name='studies'),
    path('studies/<int:pk>/', views.StudyDetailView.as_view(), name='study_detail'),
    path('publications/', views.PublicationListView.as_view(), name='publications'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('network/', views.research_network, name='network'),
    path('dataset/<int:dataset_id>/analysis/', views.dataset_analysis, name='dataset_analysis'),
    path('export/<str:format_type>/', views.export_data, name='export_data'),
]
