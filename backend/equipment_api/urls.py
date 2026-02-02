"""
URL routing for Equipment API endpoints
Defines all available API routes for the Chemical Equipment Parameter Visualizer
"""

from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # CSV upload and processing
    path('upload/', views.upload_csv, name='upload_csv'),
    
    # Upload history - returns last 5 uploads
    path('history/', views.get_upload_history, name='upload_history'),
    
    # Specific upload details
    path('upload/<int:upload_id>/', views.get_upload_detail, name='upload_detail'),
    
    # PDF report generation
    path('report/<int:upload_id>/', views.generate_pdf, name='generate_pdf'),
]
